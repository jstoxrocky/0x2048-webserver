import React, { useState } from 'react';
import { StageContext, UserContext } from '../../contexts';
import Play from './stages/play';
import Pay from './stages/pay';
import Waiting from './stages/waiting';
import MetamaskError from './stages/metamask-error';
import PaymentSuccess from './stages/payment-success';
import styled from 'styled-components';
import * as constants from '../../constants';
import FetchPaymentCodeError from './stages/fetch-payment-code-error';
import PaymentConfirmationError from './stages/payment-confirmation-error';

const Box = styled.div`
    margin: 0;
    padding: 0;

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

export const Payment = (): JSX.Element => {
    const [stage, setStage] = useState<string>(constants.WELCOME);
    const stageValue = { stage, setStage };
    const [user, setUser] = useState<string>('');
    const userValue = { user, setUser };
    return (
        <Box>
            <StageContext.Provider value={stageValue}>
                <UserContext.Provider value={userValue}>
                    {stage === constants.WELCOME && <Play />}
                    {stage === constants.PROMPT_PAYMENT && <Pay />}
                    {stage === constants.WAITING && <Waiting />}
                    {stage === constants.METAMASK_ERROR && <MetamaskError />}
                    {stage === constants.FETCH_PAYMENT_CODE_ERROR && <FetchPaymentCodeError />}
                    {stage === constants.PAYMENT_CONFIRMATION_ERROR && <PaymentConfirmationError />}
                    {stage === constants.PAYMENT_SUCCESS && <PaymentSuccess />}
                </UserContext.Provider>
            </StageContext.Provider>
        </Box>
    );
};

export default Payment;
