import { provider } from 'web3-core/types';

interface JsonRpcRequest {
    method: string;
    params: string[];
    from: string;
}

interface SendAsyncResponse {
    result: string;
}
type sendAsyncCallback = (err: string, response: SendAsyncResponse) => void;

export type MetamaskProvider = provider & {
    enable: () => Promise<string[]>;
    isMetaMask: () => boolean;
    sendAsync: (request: JsonRpcRequest, callback: sendAsyncCallback) => void;
    autoRefreshOnNetworkChange: boolean;
};

export interface EthereumWindow extends Window {
    ethereum: MetamaskProvider;
}

export interface PaymentCodeData {
    session_id: string;
    payment_code: string;
}

export interface Gamestate {
    board: number[][];
    signedScore: SignedScore;
    score: number;
}

export interface SignedScore {
    v: string;
    r: string;
    s: string;
}

export interface FakeResponse {
    data: null;
}

export interface ProtectedError {
    error: boolean;
}

export interface Block {
    from: string;
}

export interface Session {
    id: string;
    gamestate: Gamestate;
    signedScore: SignedScore;
    price: EthUsd;
    paid: boolean;
}

export type Accounts = string[];

export interface EthUsd {
    eth: string;
    usd: string;
}

export interface Metadata {
    highscore: string;
    jackpot: EthUsd;
    price: EthUsd;
}
