import { ProtectedError, EthereumWindow, Accounts } from '../types';
import protectedCall from './protected-call';

declare const window: EthereumWindow;

export interface ProtectedAccounts extends ProtectedError {
    response: Accounts | null;
}

const fetchAccount = (): Promise<Accounts> => {
    if (typeof window.ethereum === 'undefined') {
        throw 'No Ethereum provider detected';
    } else if (!window.ethereum.isMetaMask) {
        throw 'Metamask is not installed';
    }
    const { ethereum } = window;
    const promiseAccounts: Promise<Accounts> = ethereum.enable();
    return promiseAccounts;
};

const protectedFetchAccount = async (): Promise<ProtectedAccounts> => {
    const protectedAccounts: ProtectedAccounts = await protectedCall<Accounts>(fetchAccount());
    return protectedAccounts;
};

export default protectedFetchAccount;
