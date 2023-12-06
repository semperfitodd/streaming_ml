import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './search-topic.styles.css';

const SearchTopic = () => {
    const [inputValue, setInputValue] = useState('');
    const apiEndpoint = 'https://mecji43lle.execute-api.us-east-1.amazonaws.com/producer'; // Replace with your API endpoint

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = async () => {
        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ search_query: inputValue }), // Corrected data structure
            });

            if (response.ok) {
                const jsonResponse = await response.json();
                console.log('Response:', jsonResponse);
                // Handle the response as needed
            } else {
                console.error('Request failed with status:', response.status);
            }
        } catch (error) {
            console.error('Request failed:', error);
        }
    };

    return (
        <div className="container">
            <div className="row justify-content-center align-items-center vh-100">
                <div className="col-md-6">
                    <form onSubmit={handleSubmit}>
                        <div className="input-group mb-3">
                            <input type="text" className="form-control" value={inputValue} onChange={handleInputChange} placeholder="Twitter Topic" />
                            <button className="btn btn-info" onClick={handleSubmit}>Go</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default SearchTopic;
