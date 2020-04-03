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
};

export interface EthereumWindow extends Window {
    ethereum: MetamaskProvider;
}

export interface ChallengeData {
    session_id: string;
    challenge: string;
}
export type TransactionHash = string;
export type SignedChallenge = string;

export interface PendingChallenge {
    transactionHash: string;
    signedChallenge: string;
}

export interface Gamestate {
    score: number;
}

export interface FakeResponse {
    data: null;
}

export interface Protected {
    error: string | null;
}
