import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HealthcareChat from "./pages/HealthcareChat";
import { Toaster } from "./components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HealthcareChat />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </div>
  );
}

export default App;