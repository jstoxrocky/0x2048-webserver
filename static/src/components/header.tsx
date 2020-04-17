import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { protectedGameInfo as gameInfo } from '../logic/contract';
import { GameInfo } from '../types';

const Head = styled.h1`
    margin: 20px 0px;
    font-family: ${(props): string => props.theme.fontFamily};
    display: inline;
`;

const Div = styled.h3`
    margin: 20px 0px;
    font-family: ${(props): string => props.theme.fontFamily};
    display: inline;
    margin-left: 20px;
`;

const Header = (): JSX.Element => {
    const [stats, setStats] = useState<JSX.Element[]>([]);

    useEffect((): void => {
        const asyncFetchGameInfo = async (): Promise<void> => {
            const { response } = await gameInfo();
            const { highscore, jackpot, price } = response as GameInfo;
            const stats = [
                <Div key={0}>Highscore: {highscore}</Div>,
                <Div key={1}>Jackpot: {jackpot} ETH</Div>,
                <Div key={2}>Price: {price} ETH</Div>,
            ];
            setStats(stats);
        };
        asyncFetchGameInfo();
    }, []);

    return (
        <>
            <Head>Arcade</Head>
            {stats}
        </>
    );
};

export default Header;
