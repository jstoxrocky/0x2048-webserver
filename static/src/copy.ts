import { EthUsd } from './types';

export const METAMASK_ERROR = `there was an issue connecting to metamask`;
export const FETCH_PAYMENT_CODE_ERROR = `there was a problem fetching your payment code`;
export const PAYMENT_CONFIRMATION_ERROR = `there was a problem confirming your payment`;
export const PROMPT_PAYMENT = (price: EthUsd): string => `${price.eth} eth (${price.usd} usd) per play`;
export const WAITING = `waiting for payment confirmation...`;
export const WELCOME = `get a highscore and win the jackpot`;
export const PAYMENT_SUCCESS = `payment confirmed`;
