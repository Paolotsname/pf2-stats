import { StrictMode } from "react";
import { createRoot, Root } from "react-dom/client";
import App from "./App";

// Ensure the root element exists and assert its type as HTMLElement
const rootElement: HTMLElement | null = document.getElementById("root");

if (!rootElement) {
    throw new Error("Root element not found");
}

// Create a root instance
const root: Root = createRoot(rootElement);

// Render the application
root.render(
    <StrictMode>
        <App />
    </StrictMode>
);
