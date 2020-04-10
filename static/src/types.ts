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

export interface PaymentCodeData {
    session_id: string;
    payment_code: string;
}

export interface GameResponse {
    gamestate: Gamestate;
    signed_score: SignedScore;
}

export interface Gamestate {
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
    id: string | null;
    gamestate: Gamestate | null;
    signedScore: SignedScore | null;
}

export type Accounts = string[];

export interface Metadata {
    highscore: number;
    jackpot: number;
    price: number;
    round: number;
}

export interface GameInfo {
    id: string;
    highscore: number;
    jackpot: number;
    name: string;
}

export interface GameInfoResponse {
    games: GameInfo[];
}
