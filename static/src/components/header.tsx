import React, { useState, useEffect, useContext } from 'react';
import styled from 'styled-components';
import fetchMetadata from './payment/logic/fetch-metadata';
import { Metadata, EthUsd } from '../types';
import { SessionContext } from '../contexts';

const FlexParent = styled.div`
    margin: 0;
    padding: 0;

    display: flex;
    justify-content: flex-start;
    align-items: baseline;
    margin-top: 1rem;
    margin-left: 1.5rem;
    @media (max-width: 375px) {
        display: block;
    }
`;

const Title = styled.p`
    margin: 0;
    padding: 0;

    font-size: 2rem;
`;

const Stat = styled.div`
    margin: 0;
    padding: 0;

    font-size: 1.2rem;
    height: 1.2rem;
    margin-left: 1.5rem;

    @media (max-width: 375px) {
        margin-top: 0.3rem;
        margin-left: 0;
        font-size: 1.1rem;
        height: 1.1rem;
    }
`;

const LittleStat = styled.p`
    margin: 0;
    padding: 0;

    display: inline;
    font-size: 0.8rem;

    @media (max-width: 375px) {
        font-size: 0.75rem;
    }
`;

const GreyBox = styled.span`
    margin: 0;
    padding: 0;

    display: inline-block;
    width: 4rem;
    width: ${(props: { width: string }): string => props.width}rem;
    height: 1.2rem;
    background-color: #f2f2f2;

    &:last-child {
        margin-left: 0.5rem;
    }

    @media (max-width: 375px) {
        margin-top: 0.3rem;
        margin-left: 0;
        height: 1.1rem;
    }
`;

const MockStatsContainer = styled.span`
    display: flex;
    justify-content: flex-start;
    align-items: baseline;

    @media (max-width: 375px) {
        display: block;
    }
`;

const MockStatContainer = styled.span`
    margin: 0;
    padding: 0;

    margin-right: 1.5rem;

    &:first-child {
        margin-left: 1.5rem;
    }

    &:last-child {
        margin-right: 0;
    }

    @media (max-width: 375px) {
        display: block;
        margin-right: 0;

        &:first-child {
            margin-left: 0;
        }
    }
`;

const MockStat = (props: { labelWidth: string; statWidth: string }): JSX.Element => (
    <MockStatContainer>
        <GreyBox width={props.labelWidth} />
        <GreyBox width={props.statWidth} />
    </MockStatContainer>
);

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
    const mockHighscore = <MockStat labelWidth={'4'} statWidth={'3'} />;
    const mockJackpot = <MockStat labelWidth={'3'} statWidth={'9'} />;
    const mockPrice = <MockStat labelWidth={'2.5'} statWidth={'9'} />;
    const initialStats = [mockHighscore, mockJackpot, mockPrice];
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
            <MockStatsContainer>{stats}</MockStatsContainer>
        </FlexParent>
    );
};

export default Header;
