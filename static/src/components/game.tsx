import React from 'react';
import styled from 'styled-components';

const Square = styled.div`
    margin-left: 1.5rem;
    margin-right: 1.5rem;
    margin-top: 1rem;
    border: 1px solid;
    &::after {
        content: '';
        display: block;
        padding-bottom: 100%;
    }
`;

const Content = styled.div`
    position: absolute;
    height: 100%;
`;

const Game = (): JSX.Element => {
    return (
        <Square>
            <Content />
        </Square>
    );
};

export default Game;
