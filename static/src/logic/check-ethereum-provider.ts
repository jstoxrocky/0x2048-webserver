import { Protected, EthereumWindow } from '../types';

declare const window: EthereumWindow;

const checkEthereumProvider = (): Protected => {
    let error = null;
    if (typeof window.ethereum === 'undefined') {
        error = 'No Ethereum provider detected';
    } else if (!window.ethereum.isMetaMask) {
        error = 'Metamask is not installed';
    }
    return { error };
};

export default checkEthereumProvider;
