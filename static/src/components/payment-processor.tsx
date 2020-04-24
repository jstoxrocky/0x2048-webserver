import React, { useContext, useState } from 'react';
import styled from 'styled-components';
import { PaymentCodeData, GameResponse, Accounts } from '../types';
import sessionContext from '../session-context';
import fetchAccount from '../logic/fetch-account';
import fetchPaymentCode from '../logic/fetch-payment-code';
import confirmPaymentAndFetchGame from '../logic/fetch-payment-confirmation';
import { protectedPay as pay } from '../logic/contract';
import {
    METAMASK_ERROR,
    FETCH_PAYMENT_CODE_ERROR,
    PAYMENT_CONFIRMATION_ERROR,
    NEW_GAME_MESSAGE,
    WAITING_FOR_PAYMENT_MESSAGE,
    WELCOME_MESSAGE,
    SUCCESSFUL_PAYMENT_MESSAGE,
} from '../copy';

interface ButtonProps {
    primary?: boolean;
}

interface ResetButtonProps {
    children: string;
}

interface ReconfirmButtonProps {
    address: string;
    sessionId: string;
}

const Box = styled.div`
    display: grid;
    grid-template-areas:
        'txt txt'
        'btn btn';
    border: 1px solid;
    padding: 1rem;
    font-family: ${(props): string => props.theme.fontFamily};
    margin: 0 1.5rem;
    margin-top: 1rem;
`;

const Text = styled.p`
    margin: 0;
    grid-area: txt;
    font-size: 1.2rem;
    margin-top: 0;
`;

const Button = styled.button`
    margin-right: 0.75rem;
    margin-bottom: 0;
    margin-top: 0.75rem;
    padding-right: 0.75rem;
    padding: 0.125rem;
    padding-bottom: 0.25rem;
    border-style: none;
    width: 10%;
    background-color: ${(props: ButtonProps): string => (props.primary ? 'black' : 'white')};
    color: ${(props: ButtonProps): string => (props.primary ? 'white' : 'black')};
    border-style: ${(props: ButtonProps): string => (props.primary ? 'none' : 'solid')};
    border-width: 1px;
    border-color: black;
    @media (max-width: 768px) {
        width: 40%;
    }
`;

const Buttons = styled.div`
    grid-area: btn;
    display: flex;
    justify-content: left;
`;

const PaymentProcessor = (): JSX.Element => {
    const { session, setSession } = useContext(sessionContext);
    const initialMessage = WELCOME_MESSAGE;
    const [message, setMessage] = useState<string[]>(initialMessage);

    const onClickPay = async (): Promise<void> => {
        const { error: metamaskError, response: accounts } = await fetchAccount();
        if (metamaskError) {
            const buttons = [<ResetButton key={0}>Ok</ResetButton>];
            setMessage(METAMASK_ERROR);
            setButtons(buttons);
            return;
        }
        const [user] = accounts as Accounts;

        const { error: paymentCodeError, data: paymentCodeData } = await fetchPaymentCode();
        if (paymentCodeError) {
            const buttons = [<ResetButton key={0}>Ok</ResetButton>];
            setMessage(FETCH_PAYMENT_CODE_ERROR);
            setButtons(buttons);
            return;
        }
        const paymentCode = (paymentCodeData as PaymentCodeData).payment_code;
        const sessionId = (paymentCodeData as PaymentCodeData).session_id;

        const { error: transactionError } = await pay(paymentCode);
        if (transactionError) {
            const buttons = [
                <ReconfirmPaymentButton key={0} address={user} sessionId={sessionId} />,
                <ResetButton key={1}>cancel</ResetButton>,
            ];
            setMessage(PAYMENT_CONFIRMATION_ERROR);
            setButtons(buttons);
            return;
        }

        const { error: confirmationError, data: gameData } = await confirmPaymentAndFetchGame(user, sessionId);
        if (confirmationError) {
            const buttons = [
                <ReconfirmPaymentButton key={0} address={user} sessionId={sessionId} />,
                <ResetButton key={1}>cancel</ResetButton>,
            ];
            setMessage(PAYMENT_CONFIRMATION_ERROR);
            setButtons(buttons);
            return;
        }
        setMessage(SUCCESSFUL_PAYMENT_MESSAGE);
        setButtons([]);
        const gamestate = (gameData as GameResponse).gamestate;
        const signedScore = (gameData as GameResponse).signed_score;
        setSession({ ...session, id: sessionId, gamestate, signedScore });
        // set gameId here too ^
    };

    const GameButton = (): JSX.Element => {
        const label = 'play';
        return (
            <Button
                primary
                onClick={(): void => {
                    const buttons = [<PaymentButton key={0} />, <ResetButton key={1}>cancel</ResetButton>];
                    setMessage(NEW_GAME_MESSAGE);
                    setButtons(buttons);
                }}
            >
                {label}
            </Button>
        );
    };

    const PaymentButton = (): JSX.Element => {
        return (
            <Button
                primary
                onClick={(): void => {
                    // setState must come before onClickPay
                    setMessage(WAITING_FOR_PAYMENT_MESSAGE);
                    setButtons([]);
                    onClickPay();
                }}
            >
                pay
            </Button>
        );
    };

    const ReconfirmPaymentButton = (props: ReconfirmButtonProps): JSX.Element => {
        const { address, sessionId } = props;
        const confirmButton = (
            <Button
                primary
                onClick={async (): Promise<void> => {
                    const { error: confirmationError, data: gameData } = await confirmPaymentAndFetchGame(
                        address,
                        sessionId,
                    );
                    if (confirmationError) {
                        const buttons = [
                            <ReconfirmPaymentButton key={0} address={address} sessionId={sessionId} />,
                            <ResetButton key={1}>cancel</ResetButton>,
                        ];
                        setMessage(PAYMENT_CONFIRMATION_ERROR);
                        setButtons(buttons);
                        return;
                    }

                    setMessage(SUCCESSFUL_PAYMENT_MESSAGE);
                    setButtons([]);

                    const gamestate = (gameData as GameResponse).gamestate;
                    const signedScore = (gameData as GameResponse).signed_score;
                    setSession({ ...session, id: sessionId, gamestate, signedScore });
                }}
            >
                reconfirm
            </Button>
        );
        return confirmButton;
    };

    const ResetButton = (props: ResetButtonProps): JSX.Element => (
        <Button
            onClick={(): void => {
                setButtons(initialButtons);
                setMessage(WELCOME_MESSAGE);
            }}
        >
            {props.children}
        </Button>
    );

    const initialButtons = [<GameButton key={0} />];
    const [buttons, setButtons] = useState<JSX.Element[]>(initialButtons);

    const text = message.map((m) => <Text key={m}>{m}</Text>);
    return (
        <Box>
            {text}
            <Buttons>{buttons}</Buttons>
        </Box>
    );
};

export default PaymentProcessor;
