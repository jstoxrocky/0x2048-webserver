import React, { useContext } from 'react';
import { StageContext } from '../../../contexts';
import { Text, ButtonWrapper, Button } from './styles/styles';
import * as copy from '../../../copy';
import * as constants from '../../../constants';

const Play = (): JSX.Element => {
    const { setStage } = useContext(StageContext);
    return (
        <>
            <Text>{copy.WELCOME}</Text>
            <ButtonWrapper>
                <Button onClick={(): void => setStage(constants.PROMPT_PAYMENT)}>play</Button>
            </ButtonWrapper>
        </>
    );
};

export default Play;
