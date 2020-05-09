import React, { useContext } from 'react';
import { StageContext } from '../../../contexts';
import { Text, ButtonWrapper, Button } from './styles/styles';
import * as copy from '../../../copy';
import * as constants from '../../../constants';

const FetchPaymentCodeError = (): JSX.Element => {
    const { setStage } = useContext(StageContext);
    return (
        <>
            <Text>{copy.FETCH_PAYMENT_CODE_ERROR}</Text>
            <ButtonWrapper>
                <Button onClick={(): void => setStage(constants.WELCOME)}>ok</Button>
            </ButtonWrapper>
        </>
    );
};

export default FetchPaymentCodeError;
