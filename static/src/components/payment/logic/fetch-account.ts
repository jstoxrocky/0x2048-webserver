import { ProtectedError, EthereumWindow, Accounts } from '../../../types';

declare const window: EthereumWindow;

export interface ProtectedAccounts extends ProtectedError {
    data: Accounts | null;
}

const fetchAccount = (): Promise<Accounts> => {
    if (typeof window.ethereum === 'undefined') {
        throw 'No Ethereum provider detected';
    } else if (!window.ethereum.isMetaMask) {
        throw 'Metamask is not installed';
    }
    const { ethereum } = window;
    ethereum.autoRefreshOnNetworkChange = false;
    const promiseAccounts: Promise<Accounts> = ethereum.enable();
    return promiseAccounts;
};

const protectedFetchAccount = async (): Promise<ProtectedAccounts> => {
    try {
        return { error: false, data: await fetchAccount() };
    } catch {
        return { error: true, data: null };
    }
};

export default protectedFetchAccount;
