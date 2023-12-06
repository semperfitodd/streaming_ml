import logo from './logo.svg';
import './App.css';
import ParticlesBg from 'particles-bg'
import SearchTopic from './components/search-topic/search-topic.component';

const config = {
};



function App() {
  return (
    <div className="App">
      <ParticlesBg type="cobweb" bg={true} num={250} color="#ffffff" />

      <SearchTopic />
    </div>
  );
}

export default App;
