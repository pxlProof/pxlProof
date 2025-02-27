import { ConnectButton } from "@rainbow-me/rainbowkit";
import "./Header.css";

export default function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <div className="logo-section">
          <h1>PxlProof</h1>
        </div>
        <div className="wallet-section">
          <ConnectButton />
        </div>
      </div>
    </header>
  );
}
