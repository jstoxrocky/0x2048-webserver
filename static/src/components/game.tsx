import React from 'react';
import styled from 'styled-components';

// * {
//     margin: 0;
//     padding: 0;
//   }

const Square = styled.div`
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    /* margin-left: 1.5rem; */
    /* margin-right: 1.5rem; */
    /* margin-top: 1rem; */
    border: 1px solid;
    &::after {
        content: '';
        display: inline-block;
        padding-bottom: 100%;
    }
`;

const Tile = styled.div`
    background-color: red;
    border: 1px solid black;
`;

const Game = (): JSX.Element => {
    return (
        <Square>
            <Tile />
            <Tile />
            <Tile />
            <Tile />
        </Square>
    );
};

export default Game;
