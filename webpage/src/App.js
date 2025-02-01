import { useState } from "react";
import "./styles.css";

function PickLevel({ label, value, onChange }) {
    return (
        <label>
        {label}:
        <input type="number" value={value} onChange={onChange} />
        </label>
    );
}

function PickClass() {
    return (
        <label>
        Pick a fruit:
        <select name="selectedFruit">
        <option value="alchemist">Alchemist</option>
        <option value="ranger">Ranger</option>
        </select>
        </label>
    );
}

export default function App() {
    const [playerLevel, setPlayerLevel] = useState(0);
    const [enemyLevel, setEnemyLevel] = useState(0);

    return (
        <div>
        <div className="form-container">
        <PickLevel
        label="Player level"
        value={playerLevel}
        onChange={(e) => setPlayerLevel(Number(e.target.value))}
        />

        <PickClass />

        <PickLevel
        label="Enemy level"
        value={enemyLevel}
        onChange={(e) => setEnemyLevel(Number(e.target.value))}
        />
        </div>
        <h3>amogus {playerLevel + enemyLevel}</h3>
        </div>
    );
}
