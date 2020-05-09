import React, { useContext } from 'react';
import styled from 'styled-components';
import { SessionContext } from '../contexts';

const Container = styled.div`
    margin: 0;
    padding: 0;

    display: flex;
    margin-top: 1rem;
    margin-left: 1.5rem;
    margin-right: 1.5rem;
    border: solid black 1px;
    padding: 1.5rem;

    @media (max-width: 375px) {
        border: none;
        padding: 0;
    }
`;

const Board = styled.div`
    margin: 0;
    padding: 0;

    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    grid-gap: 5px;
    width: 35%;

    @media (max-width: 375px) {
        width: 100%;
    }
`;

const Tile = styled.div`
    margin: 0;
    padding: 0;

    border: solid black 1px;
    font-size: 2rem;

    &::before {
        content: '';
        padding-bottom: 100%;
        display: inline-block;
        padding-left: 70%;
    }
`;

const Game = (): JSX.Element => {
    const {
        session: {
            gamestate: { board },
        },
    } = useContext(SessionContext);
    const [row1, row2, row3, row4] = board;
    return (
        <Container>
            <Board>
                <Tile>{row1[0]}</Tile>
                <Tile>{row1[1]}</Tile>
                <Tile>{row1[2]}</Tile>
                <Tile>{row1[3]}</Tile>
                <Tile>{row2[0]}</Tile>
                <Tile>{row2[1]}</Tile>
                <Tile>{row2[2]}</Tile>
                <Tile>{row2[3]}</Tile>
                <Tile>{row3[0]}</Tile>
                <Tile>{row3[1]}</Tile>
                <Tile>{row3[2]}</Tile>
                <Tile>{row3[3]}</Tile>
                <Tile>{row4[0]}</Tile>
                <Tile>{row4[1]}</Tile>
                <Tile>{row4[2]}</Tile>
                <Tile>{row4[3]}</Tile>
            </Board>
        </Container>
    );
};

export default Game;
