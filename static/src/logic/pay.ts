import Web3 from 'web3';
import { AbiItem } from 'web3-utils';
import { Block, ProtectedError, EthereumWindow } from '../types';
import protectedCall from './protected-call';

declare const window: EthereumWindow;

export interface ProtectedBlock extends ProtectedError {
    response: Block | null;
}

const address = '0x6097038687bed106f87DB3fF9d96e71933526C98';
const abi: AbiItem[] = [
    { inputs: [], stateMutability: 'nonpayable', type: 'constructor' },
    {
        inputs: [{ internalType: 'bytes32', name: 'gameId', type: 'bytes32' }],
        name: 'getHighscore',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'bytes32', name: 'gameId', type: 'bytes32' }],
        name: 'getJackpot',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [
            { internalType: 'bytes32', name: 'gameId', type: 'bytes32' },
            { internalType: 'address', name: 'addr', type: 'address' },
        ],
        name: 'getPaymentCode',
        outputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        name: 'highscores',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        name: 'jackpots',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
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
        inputs: [
            { internalType: 'bytes32', name: 'gameId', type: 'bytes32' },
            { internalType: 'bytes32', name: 'paymentCode', type: 'bytes32' },
        ],
        name: 'pay',
        outputs: [],
        stateMutability: 'payable',
        type: 'function',
    },
    {
        inputs: [
            { internalType: 'bytes32', name: '', type: 'bytes32' },
            { internalType: 'address', name: '', type: 'address' },
        ],
        name: 'paymentCodes',
        outputs: [{ internalType: 'bytes32', name: '', type: 'bytes32' }],
        stateMutability: 'view',
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
        inputs: [
            { internalType: 'uint8', name: 'v', type: 'uint8' },
            { internalType: 'bytes32', name: 'r', type: 'bytes32' },
            { internalType: 'bytes32', name: 's', type: 'bytes32' },
            { internalType: 'uint256', name: 'score', type: 'uint256' },
            { internalType: 'bytes32', name: 'gameId', type: 'bytes32' },
        ],
        name: 'uploadScore',
        outputs: [],
        stateMutability: 'nonpayable',
        type: 'function',
    },
];

const pay = async (gameId: string, paymentCode: string): Promise<Block> => {
    const { ethereum } = window;
    const web3 = new Web3(ethereum);
    const promiseAccount: Promise<string[]> = ethereum.enable();
    const contract = new web3.eth.Contract(abi, address);
    const promisePrice: Promise<number> = contract.methods.price().call();
    const [[account], price] = await Promise.all([promiseAccount, promisePrice]);
    const promise: Promise<Block> = contract.methods.pay(gameId, paymentCode).send({ from: account, value: price });
    return promise;
};

const protectedPay = async (gameId: string, paymentCode: string): Promise<ProtectedBlock> => {
    const protectedTransactionHash: ProtectedBlock = await protectedCall<Block>(pay(gameId, paymentCode));
    return protectedTransactionHash;
};

export default protectedPay;
