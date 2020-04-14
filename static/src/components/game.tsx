import React from 'react';
import { Gamestate } from '../types';
import styled from 'styled-components';

interface GameProps {
    gamestate: Gamestate | null;
}

const Div = styled.div`
    border: 1px solid;
    height: 400px;
    padding: 10px;
    font-family: ${(props): string => props.theme.fontFamily};
    margin-top: 10px;
`;

const Game = (props: GameProps): JSX.Element => {
    const { gamestate } = props;
    if (gamestate) {
        const { score } = gamestate as Gamestate;
        return (
            <Div>
                <h3>Score: {score}</h3>
            </Div>
        );
    }
    return <></>;
};

export default Game;
