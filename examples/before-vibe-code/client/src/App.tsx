import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { StudioPage } from './pages/StudioPage';
import { ContactPage } from './pages/ContactPage';
import { LoginPage } from './pages/LoginPage';
import { AccountPage } from './pages/AccountPage';

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="min-h-screen flex flex-col relative text-slate-900 selection:bg-blue-600 selection:text-white overflow-x-hidden bg-slate-50">
          {/* Subtle Clean Background */}
          <div 
            className="fixed inset-0 pointer-events-none z-0 bg-cover bg-center bg-no-repeat opacity-[0.08]"
            style={{ backgroundImage: "url('/bg-science.jpg')" }}
          />

          {/* Global Navigation Bar */}
          <Navbar />

          {/* Dynamic Route Pages */}
          <main className="flex-1 relative z-10 w-full">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route
                path="/studio"
                element={
                  <ProtectedRoute>
                    <StudioPage />
                  </ProtectedRoute>
                }
              />
              <Route path="/contact" element={<ContactPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route
                path="/account"
                element={
                  <ProtectedRoute>
                    <AccountPage />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </main>

          {/* Global Footer */}
          <Footer />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
