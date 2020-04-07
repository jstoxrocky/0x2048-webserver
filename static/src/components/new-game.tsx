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

        setPendingChallenge({ signedChallenge });
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


// try and wait...
// if not have a button like: tx wen tthrough but arcade messed up?
// try to confirm again here. again here.

// explain why tho:
// 
// To play the game you will need to pay the [arcade's smart contract]
// and then let the arcade know who you are.
// Payment will open up a metamask window.
// 

// We've given you a secret code. Payment works
// by sending 0.001 ETH to the Arcade's account along with the secret code.
// After you've paid, you've got to let us know who you are so we can 
// confirm your payment. You can do this by sending us back your signature.
// We'll confirm that your account 
//
// Secret code: [SECRET CODE]

// 
//
// To verify that you are the payer 



// 
//---------------------------------------------------
// We've sent you a game code. To get playing you must 
// submit this game code to the Arcade's contract along with 
// 0.001 ETH as payment. After that, you've got to let us know 
// who you are so we can confirm the payment. You can do this
// by signing the game code and sending it back to us.
// 
// Game code: [GAME CODE]
// 
// [Cancel] [Pay]
//---------------------------------------------------
// Waiting for payment confirmation...
//---------------------------------------------------
// Error 
// Something went wrong. You can Cancel or
// if you're sure that the transaction went through 
// you can click Sign to continue with payment confirmation.
//---------------------------------------------------
// Success
// Let us know who paid! Send us your signature so we
// can confirm the payment.
// 
// [Cancel] [Sign]
//---------------------------------------------------
// Error 
// Something went wrong. You can Cancel or
// if want to try again click Sign to retry payment confirmation.
//---------------------------------------------------
// Success
// 


// challenege and session id are thr same....
// Think of a game code as an
// identifier for a round of play.