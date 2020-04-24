import React from 'react';
import styled from 'styled-components';

const Square = styled.div`
    margin-top: 1rem;
    border: 1px solid;
    width: 50%;
    &::after {
        content: '';
        display: block;
        padding-bottom: 100%;
    }
`;

const Content = styled.div`
    position: absolute;
    width: 100%;
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
