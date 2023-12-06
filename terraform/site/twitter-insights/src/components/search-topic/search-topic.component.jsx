import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './search-topic.styles.css';

const SearchTopic = () => {
    const [inputValue, setInputValue] = useState('');
    const [responseText, setResponseText] = useState('');
    const apiEndpoint = 'https://mecji43lle.execute-api.us-east-1.amazonaws.com/producer';

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevents the default form submission behavior (clearing the console)
        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ search_query: inputValue })
            });

            if (response.ok) {
                const jsonResponse = await response.json();
                setResponseText(JSON.stringify(jsonResponse, null, 2));
            } else {
                setResponseText(`Request failed with status: ${response.status}`);
            }
        } catch (error) {
            setResponseText(`Request failed: ${error}`);
        }
    };

    const handleClear = () => {
        setInputValue('');
        setResponseText('');
    };

    return (
        <div className="container">
            <div className="row justify-content-center align-items-center vh-100">
                <div className="col-md-6">
                    <form onSubmit={handleSubmit}>
                        <div className="input-group mb-3">
                            <input type="text" className="form-control" value={inputValue} onChange={handleInputChange} placeholder="Twitter Topic" />
                        </div>
                        <div className='d-flex justify-content-center mb-3'>
                            <button className="btn btn-success me-3 btn-equal-width" type="submit">Go</button>
                            <button className="btn btn-danger btn-equal-width" type="button" onClick={handleClear}>Clear</button>
                        </div>
                    </form>
                    {responseText && (
                        <pre className="response-output">
                            {responseText}
                        </pre>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SearchTopic;

