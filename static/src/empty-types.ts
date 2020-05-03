import * as types from './types';

export const emptyEthUsd: types.EthUsd = {
    eth: '',
    usd: '',
};

export const emptyGamestate: types.Gamestate = {
    score: 0,
};

export const emptySignedScore: types.SignedScore = {
    v: '',
    r: '',
    s: '',
};

export const emptySession: types.Session = {
    id: '',
    gamestate: emptyGamestate,
    signedScore: emptySignedScore,
    price: emptyEthUsd,
};
