import { SignedChallenge, Protected, EthereumWindow } from '../types';
import protectedCall from './protected-call';

declare const window: EthereumWindow;
export interface ProtectedSignedChallenge extends Protected {
    response: SignedChallenge | null;
}

const typedData = {
    types: {
        EIP712Domain: [
            { name: 'name', type: 'string' },
            { name: 'version', type: 'string' },
            { name: 'chainId', type: 'uint256' },
            { name: 'verifyingContract', type: 'address' },
        ],
        Nonce: [{ name: 'nonce', type: 'bytes32' }],
    },
    primaryType: 'Nonce',
    domain: {
        name: '0x2048',
        version: '1',
        chainId: 3,
        verifyingContract: '0xF2E246BB76DF876Cef8b38ae84130F4F55De395b',
    },
    message: {
        nonce: '',
    },
};

const signChallenge = async (challenge: string): Promise<SignedChallenge> => {
    const { ethereum } = window;
    typedData.message.nonce = challenge;
    const [account] = await ethereum.enable();
    const promise: Promise<SignedChallenge> = new Promise((resolve, reject) => {
        ethereum.sendAsync(
            {
                method: 'eth_signTypedData_v4',
                params: [account, JSON.stringify(typedData)],
                from: account,
            },
            (error, response) => {
                if (error) {
                    reject();
                }
                const result: SignedChallenge = response.result;
                resolve(result);
            },
        );
    });
    return promise;
};

const protectedSignChallenge = async (challenge: string): Promise<ProtectedSignedChallenge> => {
    const errorMessage = 'Error signing';
    const signedChallenge = protectedCall<SignedChallenge>(signChallenge(challenge), errorMessage);
    return signedChallenge;
};

export default protectedSignChallenge;
