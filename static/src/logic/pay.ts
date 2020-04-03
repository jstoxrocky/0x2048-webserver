import Web3 from 'web3';
import { AbiItem } from 'web3-utils';
import { TransactionHash, Protected, EthereumWindow } from '../types';
import protectedCall from './protected-call';

declare const window: EthereumWindow;
export interface ProtectedTransactionHash extends Protected {
    response: TransactionHash | null;
}

const address = '0x8848c724B853307083F44526ad32C039b5ee1451';
const abi: AbiItem[] = [
    { inputs: [], stateMutability: 'nonpayable', type: 'constructor' },
    {
        inputs: [{ internalType: 'address', name: 'addr', type: 'address' }],
        name: 'getNonce',
        outputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [],
        name: 'highscore',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [],
        name: 'jackpot',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'address', name: '', type: 'address' }],
        name: 'nonces',
        outputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [],
        name: 'owner',
        outputs: [{ internalType: 'address', name: '', type: 'address' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'bytes32', name: 'nonce', type: 'bytes32' }],
        name: 'pay',
        outputs: [],
        stateMutability: 'payable',
        type: 'function',
    },
    {
        inputs: [],
        name: 'price',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [],
        name: 'round',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [
            { internalType: 'uint8', name: 'v', type: 'uint8' },
            { internalType: 'bytes32', name: 'r', type: 'bytes32' },
            { internalType: 'bytes32', name: 's', type: 'bytes32' },
            { internalType: 'uint256', name: 'score', type: 'uint256' },
        ],
        name: 'uploadScore',
        outputs: [],
        stateMutability: 'nonpayable',
        type: 'function',
    },
];

const pay = async (challenge: string): Promise<TransactionHash> => {
    const { ethereum } = window;
    const web3 = new Web3(ethereum);
    const contract = new web3.eth.Contract(abi, address);
    const promiseAccount: Promise<string[]> = ethereum.enable();
    const promisePrice: Promise<number> = contract.methods.price().call();
    const [[account], price] = await Promise.all([promiseAccount, promisePrice]);
    const promise: Promise<TransactionHash> = new Promise((resolve, reject) => {
        // Creating our own promise so we need to add the catch method
        contract.methods
            .pay(challenge)
            .send({ from: account, value: price })
            .once('transactionHash', (transactionHash: TransactionHash) => {
                resolve(transactionHash);
            })
            .catch(() => {
                reject();
            });
    });
    return promise;
};

const protectedPay = async (challenge: string): Promise<ProtectedTransactionHash> => {
    const errorMessage = 'Error in payment';
    const protectedTransactionHash: ProtectedTransactionHash = await protectedCall<TransactionHash>(
        pay(challenge),
        errorMessage,
    );
    return protectedTransactionHash;
};

export default protectedPay;
