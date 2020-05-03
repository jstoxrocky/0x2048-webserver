import React, { useState, useEffect, useContext } from 'react';
import styled from 'styled-components';
import fetchMetadata from './payment/logic/fetch-metadata';
import { Metadata, EthUsd } from '../types';
import { emptyEthUsd } from '../empty-types';
import { SessionContext } from '../contexts';

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

const Highscore = (highscore: string): JSX.Element => <Stat key={0}>highscore: {highscore}</Stat>;

const Jackpot = (jackpot: EthUsd): JSX.Element => (
    <Stat key={1}>
        jackpot: {jackpot.eth} eth <LittleStat>({jackpot.usd} usd)</LittleStat>
    </Stat>
);

const Price = (price: EthUsd): JSX.Element => (
    <Stat key={2}>
        price: {price.eth} eth <LittleStat>({price.usd} usd)</LittleStat>
    </Stat>
);

const Header = (): JSX.Element => {
    const initialStats = [Highscore(''), Jackpot(emptyEthUsd), Price(emptyEthUsd)];
    const [stats, setStats] = useState<JSX.Element[]>(initialStats);
    const { session, setSession } = useContext(SessionContext);

    useEffect((): void => {
        const asyncFetchGameInfo = async (): Promise<void> => {
            const { data } = await fetchMetadata();
            const { highscore, jackpot, price } = data as Metadata;
            const stats = [Highscore(highscore), Jackpot(jackpot), Price(price)];
            setStats(stats);
            setSession({ ...session, price });
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
