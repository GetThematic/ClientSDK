# Thematic Client SDK

This package can be used to authorize and access the thematic client via API. It is a thin wrapper around the existing API endpoints.

## Scripts
```
thematic-client-auth
```
An interactive auth script is included for generating a refresh token. This token can be exchanged for an access-token each time the API is used. Access tokens have a limited lifetime so should be renewed regularly.

## Tokens
Refresh tokens have a very long lived lifetime so should be kept secret! They can be invalidated in the client UI or programatically using the API. When a refresh token is invalidated it can not be recovered.

## Example
There is an example in 'examples' of interacting with the sdk.