function validateDecimalPlaces(input) {
    const value = input.value;
    if (value.includes('.')) {
        const decimals = value.split('.')[1];
        if (decimals.length > 2) {
            input.setCustomValidity("Please enter no more than 2 decimal places.");
        } else {
            input.setCustomValidity("");
        }
    } else {
        input.setCustomValidity("");
    }
}
