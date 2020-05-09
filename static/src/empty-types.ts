import * as types from './types';

export const emptyEthUsd: types.EthUsd = {
    eth: '',
    usd: '',
};

export const emptySignedScore: types.SignedScore = {
    v: '',
    r: '',
    s: '',
};

export const emptyGamestate: types.Gamestate = {
    board: [[]],
    signedScore: emptySignedScore,
    score: 0,
};

export const emptySession: types.Session = {
    id: '',
    gamestate: emptyGamestate,
    signedScore: emptySignedScore,
    price: emptyEthUsd,
    paid: false,
};
