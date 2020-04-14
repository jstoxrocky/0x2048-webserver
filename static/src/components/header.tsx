import React from 'react';
import styled from 'styled-components';

const Head = styled.h1`
    margin: 20px 0px;
    font-family: ${(props): string => props.theme.fontFamily};
    display: inline;
`;

const Header = (): JSX.Element => {
    return (
        <>
            <Head>Arcade</Head>
        </>
    );
};

export default Header;
