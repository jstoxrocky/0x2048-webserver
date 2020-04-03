import React, { useContext, useState } from 'react';
import styled from 'styled-components';
import { SignedChallenge, TransactionHash, ChallengeData, PendingChallenge } from '../types';
import sessionContext from '../session-context';
import checkEthereumProvider from '../logic/check-ethereum-provider';
import fetchChallenge from '../logic/fetch-challenge';
import pay, { ProtectedTransactionHash } from '../logic/pay';
import signChallenge, { ProtectedSignedChallenge } from '../logic/sign-challenge';
// import confirmPayment from './confirm-payment';

const Button = styled.button`
    background-color: ${(props): string => props.theme.buttonBackgroundColor};
    font-family: ${(props): string => props.theme.fontFamily};
    font-size: ${(props): string => props.theme.fontSize};
    border: none;
    border-radius: 5px;
    padding: 7px 10px;
    color: #000000;
    &:hover {
        color: #66605c;
    }
`;

const NewGame = (): JSX.Element => {
    console.log('NewGame');
    const { session, setSession } = useContext(sessionContext);
    const initialPendingChallenge = { transactionHash: '', signedChallenge: '' };
    const [, setPendingChallenge] = useState<PendingChallenge>(initialPendingChallenge);

    const onClickNewGame = async (): Promise<void> => {
        const { error: checkEthereumProviderError } = checkEthereumProvider();
        if (checkEthereumProviderError) {
            setSession({ ...session, message: checkEthereumProviderError });
        }

        const { error: challengeError, data: challengeData } = await fetchChallenge();
        if (challengeError) {
            setSession({ ...session, message: challengeError });
            return;
        }
        const challenge = (challengeData as ChallengeData).challenge;
        const sessionId = (challengeData as ChallengeData).session_id;
        setSession({ ...session, id: sessionId });

        const promiseTransactionHash = pay(challenge);
        const promiseSignChallenge = signChallenge(challenge);
        const [transactionHashResponse, signChallengeResponse]: [
            ProtectedTransactionHash,
            ProtectedSignedChallenge,
        ] = await Promise.all([promiseTransactionHash, promiseSignChallenge]);

        const { error: transactionError, response: transactionData } = transactionHashResponse;
        if (transactionError) {
            setSession({ ...session, message: transactionError });
            return;
        }
        const transactionHash = transactionData as TransactionHash;

        const { error: signChallengeError, response: signChallengeData } = signChallengeResponse;
        if (signChallengeError) {
            setSession({ ...session, message: signChallengeError });
            return;
        }
        const signedChallenge = signChallengeData as SignedChallenge;

        setPendingChallenge({ transactionHash, signedChallenge });
    };

    // const onClickConfirmPayment = async (): Promise<void> => {
    //     const [confirmPaymentError, nullableGamestate] = await confirmPayment(pendingChallenge);
    //     if (confirmPaymentError) {
    //         setSession({ ...session, message: confirmPaymentError.message });
    //     }
    //     console.log(nullableGamestate);
    // };

    return (
        <>
            <Button
                onClick={(): void => {
                    console.log('start');
                    onClickNewGame();
                    console.log('end');
                }}
            >
                Promise New Game
            </Button>

            {/* <button
                onClick={(): Promise<void> => onClickConfirmPayment()}>
                Confirm Payment
            </button> */}
            {/* <Button>Click Me!</Button>  */}
        </>
    );
};

export default NewGame;
