import React, { useContext } from 'react';
import { StageContext, UserContext } from '../../../contexts';
import { SessionContext } from '../../../contexts';
import { Text, ButtonWrapper, Button } from './styles/styles';
import * as copy from '../../../copy';
import * as constants from '../../../constants';
import processPaymentForUser from '../logic/process-payment';
import protectedFetchAccount from '../logic/fetch-account';
import { Accounts, Gamestate } from '../../../types';

const Pay = (): JSX.Element => {
    const { session, setSession } = useContext(SessionContext);
    const { setStage } = useContext(StageContext);
    const { setUser } = useContext(UserContext);
    const onClick = async (): Promise<void> => {
        setStage(constants.WAITING);
        const { error: metamaskError, data: accounts } = await protectedFetchAccount();
        if (metamaskError) {
            setStage(constants.METAMASK_ERROR);
        }
        const [user] = accounts as Accounts;
        setUser(user);
        const { stage, gamestate } = await processPaymentForUser(user);
        setStage(stage);
        if (stage === constants.PAYMENT_SUCCESS) {
            setSession({ ...session, paid: true, gamestate: gamestate as Gamestate });
        }
    };
    return (
        <>
            <Text>{copy.PROMPT_PAYMENT(session.price)}</Text>
            <ButtonWrapper>
                <Button onClick={onClick}>pay</Button>
                <Button onClick={(): void => setStage(constants.WELCOME)}>cancel</Button>
            </ButtonWrapper>
        </>
    );
};

export default Pay;
