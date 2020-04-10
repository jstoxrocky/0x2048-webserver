import React, { useContext, useState, useEffect } from 'react';
import styled from 'styled-components';
import { PaymentCodeData, GameResponse, Accounts, GameInfoResponse } from '../types';
import sessionContext from '../session-context';
import fetchAccount from '../logic/fetch-account';
import fetchPaymentCode from '../logic/fetch-payment-code';
import fetchGameInfo from '../logic/fetch-game-info';
import confirmPaymentAndFetchGame from '../logic/fetch-game';
import pay from '../logic/pay';
import {
    METAMASK_ERROR,
    FETCH_PAYMENT_CODE_ERROR,
    TRANSACTION_ERROR,
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
    gameId: string;
    address: string;
    sessionId: string;
}

interface GameButtonProps {
    name: string;
    gameId: string;
}

interface PaymentButtonProps {
    gameId: string;
}

const Button = styled.button`
    width: 100px;
    background-color: ${(props: ButtonProps): string => (props.primary ? 'black' : 'white')};
    color: ${(props: ButtonProps): string => (props.primary ? 'white' : 'black')};
`;

const Div = styled.div`
    border: 1px solid;
    height: 100px;
    padding: 10px;
    font-family: ${(props): string => props.theme.fontFamily};
    margin-top: 20px;
`;

const Text = styled.h3`
    transform: rotate(0.5deg);
`;

const PaymentProcessor = (): JSX.Element => {
    const { session, setSession } = useContext(sessionContext);
    const [buttons, setButtons] = useState<JSX.Element[]>([]);
    const initialMessage = WELCOME_MESSAGE;
    const [message, setMessage] = useState(initialMessage);

    useEffect((): void => {
        const asyncFetchGameInfo = async (): Promise<void> => {
            const { error, data } = await fetchGameInfo();
            if (error) {
                return;
            }
            const games = (data as GameInfoResponse).games;
            const buttons = games.map((game) => <GameButton key={game.id} name={game.name} gameId={game.id} />);
            setButtons(buttons);
        };
        asyncFetchGameInfo();
    }, []);

    const onClickPay = async (gameId: string): Promise<void> => {
        const { error: metamaskError, response: accounts } = await fetchAccount();
        if (metamaskError) {
            const buttons = [<ResetButton key={0}>Ok</ResetButton>];
            setMessage(METAMASK_ERROR);
            setButtons(buttons);
            return;
        }
        const [address] = accounts as Accounts;

        const { error: paymentCodeError, data: paymentCodeData } = await fetchPaymentCode();
        if (paymentCodeError) {
            const buttons = [<ResetButton key={0}>Ok</ResetButton>];
            setMessage(FETCH_PAYMENT_CODE_ERROR);
            setButtons(buttons);
            return;
        }
        const paymentCode = (paymentCodeData as PaymentCodeData).payment_code;
        const sessionId = (paymentCodeData as PaymentCodeData).session_id;

        const { error: transactionError } = await pay(gameId, paymentCode);
        if (transactionError) {
            const buttons = [
                <ReconfirmPaymentButton key={0} gameId={gameId} address={address} sessionId={sessionId} />,
                <ResetButton key={1}>Cancel</ResetButton>,
            ];
            setMessage(TRANSACTION_ERROR);
            setButtons(buttons);
            return;
        }

        const { error: confirmationError, data: gameData } = await confirmPaymentAndFetchGame(
            gameId,
            address,
            sessionId,
        );
        if (confirmationError) {
            const buttons = [
                <ReconfirmPaymentButton key={0} gameId={gameId} address={address} sessionId={sessionId} />,
                <ResetButton key={1}>Cancel</ResetButton>,
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

    const GameButton = (props: GameButtonProps): JSX.Element => {
        const { name, gameId } = props;
        const label = 'Play ' + name;
        return (
            <Button
                primary
                onClick={(): void => {
                    const buttons = [
                        <PaymentButton key={0} gameId={gameId} />,
                        <ResetButton key={1}>Cancel</ResetButton>,
                    ];
                    setMessage(NEW_GAME_MESSAGE);
                    setButtons(buttons);
                }}
            >
                {label}
            </Button>
        );
    };

    const PaymentButton = (props: PaymentButtonProps): JSX.Element => {
        const { gameId } = props;
        return (
            <Button
                primary
                onClick={(): void => {
                    // setState must come before onClickPay
                    setMessage(WAITING_FOR_PAYMENT_MESSAGE);
                    setButtons([]);
                    onClickPay(gameId);
                }}
            >
                Pay
            </Button>
        );
    };

    const ReconfirmPaymentButton = (props: ReconfirmButtonProps): JSX.Element => {
        const { gameId, address, sessionId } = props;
        const confirmButton = (
            <Button
                primary
                onClick={async (): Promise<void> => {
                    const { error: confirmationError, data: gameData } = await confirmPaymentAndFetchGame(
                        gameId,
                        address,
                        sessionId,
                    );
                    if (confirmationError) {
                        const buttons = [
                            <ReconfirmPaymentButton key={0} gameId={gameId} address={address} sessionId={sessionId} />,
                            <ResetButton key={1}>Cancel</ResetButton>,
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
                Confirm
            </Button>
        );
        return confirmButton;
    };

    const ResetButton = (props: ResetButtonProps): JSX.Element => (
        <Button
            onClick={(): void => {
                const asyncFetchGameInfo = async (): Promise<void> => {
                    const { error, data } = await fetchGameInfo();
                    if (error) {
                        return;
                    }
                    const games = (data as GameInfoResponse).games;
                    const buttons = games.map((game) => <GameButton key={game.id} name={game.name} gameId={game.id} />);
                    setButtons(buttons);
                };
                asyncFetchGameInfo();
                setMessage(WELCOME_MESSAGE);
            }}
        >
            {props.children}
        </Button>
    );

    return (
        <Div>
            <Text>{message}</Text>
            <div>{buttons}</div>
        </Div>
    );
};

export default PaymentProcessor;
