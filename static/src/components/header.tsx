import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { protectedGameInfo as gameInfo } from '../logic/contract';
import { GameInfo } from '../types';

const FlexParent = styled.div`
    display: flex;
    justify-content: flex-start;
    align-items: baseline;
    margin-top: 1rem;
    margin-left: 1.5rem;
    @media (max-width: 768px) {
        display: block;
    }
`;

const Title = styled.p`
    margin: 0;
    font-size: 2rem;
`;

const Stat = styled.p`
    margin: 0;
    font-size: 1.2rem;
    margin-left: 1.5rem;
    @media (max-width: 768px) {
        margin-top: 0.3rem;
        margin-left: 0;
        font-size: 1.1rem;
    }
`;

const LittleStat = styled.p`
    display: inline;
    font-size: 0.8rem;
    @media (max-width: 768px) {
        font-size: 0.75rem;
    }
`;

const Header = (): JSX.Element => {
    const [stats, setStats] = useState<JSX.Element[]>([]);

    useEffect((): void => {
        const asyncFetchGameInfo = async (): Promise<void> => {
            // https://api.gemini.com/v1/pubticker/ethusd
            const { response } = await gameInfo();
            const { highscore, jackpot, price } = response as GameInfo;
            const stats = [
                <Stat key={0}>highscore: {highscore}</Stat>,
                <Stat key={1}>
                    jackpot: {jackpot} eth <LittleStat>(573.25 usd)</LittleStat>
                </Stat>,
                <Stat key={2}>
                    price: {price} eth <LittleStat>(0.25 usd)</LittleStat>
                </Stat>,
            ];
            setStats(stats);
        };
        asyncFetchGameInfo();
    }, []);

    return (
        <FlexParent>
            <Title>twenty forty-eight</Title>
            {stats}
        </FlexParent>
    );
};

export default Header;
