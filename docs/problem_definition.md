1. Objectives
- The project is a web app that uses a trained model to forecast SPY’s next trading day return (in percentage). 
- The app includes a service worker that includes a trained model for prediction of the return of the next trading day, based on the returns of the previous n trading days of the SPY stock (exclude market closed day - saturday/sunday/holidays).
- The prediction result will be served from the service worker through RESTful API to a Dashboard where user can pick an n days 'look back' data range, and receives the return prediction for the n+1 day.

2. Instrument and scope
- Instrument: SPY stock
- Scope: using trading day's closing price only, no in-day ticks; predict SPY next day stock return only (1 day horizon).  

3. Target definition and units
- day N predicted return percentage = ([(the SPY shares bought on day N) x (end-of-day cost per share on day N-1)] / [(the SPY shares bought on day N-1) x (end-of-day cost per share on day N-1)] - 1) x 100.
which means:
- day N predicted return rate = ([(the SPY shares bought on day N)/ (the SPY shares bought on day N-1)] - 1) x 100

*day-end cost per share is adjusted to offset price-changing effects like dividends payout, stock splittings that essentially change the prices of each stock but not the returns since investors still own the same value.
- Units are (+/-) percentage.

4. Input window
- The n consecutive days' adjusted returns

5. Example
A user selects n consecutive trading days and requests a forecast on the n+1 day.
The service:
- Retrieves the 60 daily adjusted returns available through that date.
- Runs the saved PyTorch model.
- Send back the predicted return for the n+1 day.

6. Out of scope
- Multi days prediction