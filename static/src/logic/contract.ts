import Web3 from 'web3';
import { AbiItem } from 'web3-utils';
import { Block, GameInfo, ProtectedError, EthereumWindow } from '../types';
import protectedCall from './protected-call';

declare const window: EthereumWindow;

export interface ProtectedBlock extends ProtectedError {
    response: Block | null;
}

export interface ProtectedGameInfo extends ProtectedError {
    response: GameInfo | null;
}

const gameId = '0xf709f7dcc2067e34dd3c2fdb82a42f4429cb0ea61e62a21bc6d0ce860d11032d';
const address = '0x607809129876B6637a291Ce2dEbA3D71c7ffc3E7';
const abi: AbiItem[] = [
    {
        inputs: [
            { internalType: 'bytes32', name: 'gameId', type: 'bytes32' },
            { internalType: 'uint256', name: 'price', type: 'uint256' },
            { internalType: 'uint8', name: 'percentFee', type: 'uint8' },
        ],
        name: 'addGame',
        outputs: [],
        stateMutability: 'nonpayable',
        type: 'function',
    },
    {
        inputs: [
            { internalType: 'bytes32', name: 'gameId', type: 'bytes32' },
            { internalType: 'uint256', name: 'score', type: 'uint256' },
            { internalType: 'uint8', name: 'v', type: 'uint8' },
            { internalType: 'bytes32', name: 'r', type: 'bytes32' },
            { internalType: 'bytes32', name: 's', type: 'bytes32' },
        ],
        name: 'claimHighscore',
        outputs: [],
        stateMutability: 'nonpayable',
        type: 'function',
    },
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
        inputs: [{ internalType: 'bytes32', name: 'gameId', type: 'bytes32' }],
        name: 'getOwner',
        outputs: [{ internalType: 'address', name: '', type: 'address' }],
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
        inputs: [{ internalType: 'bytes32', name: 'gameId', type: 'bytes32' }],
        name: 'getPercentFee',
        outputs: [{ internalType: 'uint8', name: '', type: 'uint8' }],
        stateMutability: 'view',
        type: 'function',
    },
    {
        inputs: [{ internalType: 'bytes32', name: 'gameId', type: 'bytes32' }],
        name: 'getPrice',
        outputs: [{ internalType: 'uint256', name: '', type: 'uint256' }],
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
];

const pay = async (paymentCode: string): Promise<Block> => {
    const { ethereum } = window;
    const web3 = new Web3(ethereum);
    const promiseAccount: Promise<string[]> = ethereum.enable();
    const contract = new web3.eth.Contract(abi, address);
    const promisePrice: Promise<number> = contract.methods.getPrice(gameId).call();
    const [[account], price] = await Promise.all([promiseAccount, promisePrice]);
    const promise: Promise<Block> = contract.methods.pay(gameId, paymentCode).send({ from: account, value: price });
    return promise;
};

export const protectedPay = async (paymentCode: string): Promise<ProtectedBlock> => {
    const protectedTransactionHash: ProtectedBlock = await protectedCall<Block>(pay(paymentCode));
    return protectedTransactionHash;
};

const gameInfo = async (): Promise<GameInfo> => {
    const { ethereum } = window;
    const web3 = new Web3(ethereum);
    const contract = new web3.eth.Contract(abi, address);
    const promiseHighscore: Promise<number> = contract.methods.getHighscore(gameId).call();
    const promiseJackpot: Promise<number> = contract.methods.getJackpot(gameId).call();
    const promisePrice: Promise<number> = contract.methods.getPrice(gameId).call();
    const [highscore, jackpotWei, priceWei] = await Promise.all([promiseHighscore, promiseJackpot, promisePrice]);
    const jackpot = web3.utils.fromWei(jackpotWei.toString(), 'ether');
    const price = web3.utils.fromWei(priceWei.toString(), 'ether');
    return { highscore, jackpot, price };
};

export const protectedGameInfo = async (): Promise<ProtectedGameInfo> => {
    const protectedGameInfo: ProtectedGameInfo = await protectedCall<GameInfo>(gameInfo());
    return protectedGameInfo;
};
