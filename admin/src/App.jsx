import NavBar from "./components/NavBar/NavBar";
import SideBar from "./components/SideBar/SideBar";
import { Routes, Route } from 'react-router-dom';
import Add from "./pages/Add/Add";
import List from "./pages/List/List";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {

  const url = "https://cac-trabajofinal.onrender.com";

  return (
    <div>
      <ToastContainer/>
      <NavBar />
      <hr/>
      <div className="app-content">
        <SideBar />
        <Routes>
          <Route path="/add" element={<Add url={url}/>}/>
          <Route path="/list" element={<List url={url}/>}/>
        </Routes>
      </div>
    </div>
  )
}

export default App
