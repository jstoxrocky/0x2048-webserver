import styled from 'styled-components';

export const Text = styled.p`
    margin: 0;
    padding: 0;

    grid-area: txt;
    font-size: 1.2rem;
    margin-top: 0;
`;

export const Button = styled.button`
    margin: 0;
    padding: 0;

    margin-right: 0.75rem;
    margin-bottom: 0;
    margin-top: 0.75rem;
    padding-right: 0.75rem;
    padding: 0.125rem;
    padding-bottom: 0.25rem;
    border-style: none;
    width: 10%;
    background-color: ${(props: ButtonProps): string => (props.primary ? 'black' : 'white')};
    color: ${(props: ButtonProps): string => (props.primary ? 'white' : 'black')};
    border-style: ${(props: ButtonProps): string => (props.primary ? 'none' : 'solid')};
    border-width: 1px;
    border-color: black;
    @media (max-width: 375px) {
        width: 40%;
    }
`;

export const ButtonWrapper = styled.div`
    margin: 0;
    padding: 0;

    grid-area: btn;
    display: flex;
    justify-content: left;
`;

interface ButtonProps {
    primary?: boolean;
}
