import React, { useContext } from 'react';
import { StageContext, UserContext, SessionContext } from '../../../contexts';
import { Text, ButtonWrapper, Button } from './styles/styles';
import * as copy from '../../../copy';
import * as constants from '../../../constants';
import confirmPaymentAndFetchGame from '../logic/fetch-payment-confirmation';

const PaymentConfirmationError = (): JSX.Element => {
    const { setStage } = useContext(StageContext);
    const { user } = useContext(UserContext);
    const { session } = useContext(SessionContext);
    const onClick = async (): Promise<void> => {
        setStage(constants.WAITING);
        const { error: confirmationError } = await confirmPaymentAndFetchGame(user, session.id);
        if (confirmationError) {
            setStage(constants.PAYMENT_CONFIRMATION_ERROR);
        } else {
            setStage(constants.PAYMENT_SUCCESS);
        }
    };
    return (
        <>
            <Text>{copy.PAYMENT_CONFIRMATION_ERROR}</Text>
            <ButtonWrapper>
                <Button onClick={onClick}>reconfirm</Button>
                <Button onClick={(): void => setStage(constants.WELCOME)}>cancel</Button>
            </ButtonWrapper>
        </>
    );
};

export default PaymentConfirmationError;
