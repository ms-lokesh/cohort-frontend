import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Calendar, Flame, X, RefreshCw, HelpCircle, Key, Clock, User, DoorOpen } from 'lucide-react';
import './DoorKeyGame.css';

const DoorKeyGame = ({ onClose, pillarName }) => {
    const [gameState, setGameState] = useState(null);
    const [playerPosition, setPlayerPosition] = useState({ row: 2, col: 0 }); // Bottom left
    const [collectedKeys, setCollectedKeys] = useState([]);
    const [visitedCells, setVisitedCells] = useState(new Set());
    const [isComplete, setIsComplete] = useState(false);
    const [streak, setStreak] = useState(0);
    const [showRules, setShowRules] = useState(false);
    const [timeElapsed, setTimeElapsed] = useState(0); // Stopwatch in seconds
    const [gameStarted, setGameStarted] = useState(false);
    const [hitWall, setHitWall] = useState(false);
    const [message, setMessage] = useState('');

    // Stopwatch effect
    useEffect(() => {
        if (!gameStarted || isComplete) return;

        const timer = setInterval(() => {
            setTimeElapsed(prev => prev + 1);
        }, 1000);

        return () => clearInterval(timer);
    }, [gameStarted, isComplete]);

    // Format time display
    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    // Generate daily seed based on date
    const getDailySeed = useCallback(() => {
        const today = new Date();
        return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}-${pillarName}-hiddenmaze`;
    }, [pillarName]);

    // Wall pattern generators for different challenge types (must be before generateHiddenMaze)
    const createSpiralWalls = (walls, rows, cols, rand) => {
        const centerRow = Math.floor(rows / 2);
        const centerCol = Math.floor(cols / 2);
        const maxRadius = Math.min(rows, cols) / 2;

        for (let r = 1; r < maxRadius; r++) {
            if (rand() < 0.7) {
                for (let i = 0; i < 8; i++) {
                    const angle = (i / 8) * 2 * Math.PI;
                    const wallRow = Math.floor(centerRow + r * Math.sin(angle));
                    const wallCol = Math.floor(centerCol + r * Math.cos(angle));
                    if (wallRow >= 0 && wallRow < rows && wallCol >= 0 && wallCol < cols) {
                        walls[wallRow][wallCol] = 1;
                    }
                }
            }
        }
    };

    const createCrossWalls = (walls, rows, cols, rand) => {
        const midRow = Math.floor(rows / 2);
        const midCol = Math.floor(cols / 2);

        // Vertical line with gaps
        for (let row = 0; row < rows; row++) {
            if (rand() < 0.6 && !(row === rows - 1 && midCol === 0)) {
                walls[row][midCol] = 1;
            }
        }

        // Horizontal line with gaps
        for (let col = 0; col < cols; col++) {
            if (rand() < 0.6 && !(midRow === rows - 1 && col === 0)) {
                walls[midRow][col] = 1;
            }
        }
    };

    const createDiagonalWalls = (walls, rows, cols, rand) => {
        // Main diagonal
        for (let i = 0; i < Math.min(rows, cols); i++) {
            if (rand() < 0.5 && !(i === rows - 1 && i === 0)) {
                walls[i][i] = 1;
            }
        }

        // Anti-diagonal
        for (let i = 0; i < Math.min(rows, cols); i++) {
            const row = i;
            const col = cols - 1 - i;
            if (rand() < 0.5 && !(row === rows - 1 && col === 0)) {
                walls[row][col] = 1;
            }
        }
    };

    const createCornerWalls = (walls, rows, cols, rand) => {
        // Create walls near corners to make navigation tricky
        const corners = [
            { row: 0, col: 0 }, { row: 0, col: cols - 1 },
            { row: rows - 1, col: 0 }, { row: rows - 1, col: cols - 1 }
        ];

        corners.forEach(corner => {
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    const newRow = corner.row + dr;
                    const newCol = corner.col + dc;
                    if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols) {
                        if (rand() < 0.4 && !(newRow === rows - 1 && newCol === 0)) {
                            walls[newRow][newCol] = 1;
                        }
                    }
                }
            }
        });
    };

    const createRandomWalls = (walls, rows, cols, rand) => {
        const wallCount = Math.floor((rows * cols) * (0.15 + rand() * 0.2)); // 15-35% walls
        for (let i = 0; i < wallCount; i++) {
            const row = Math.floor(rand() * rows);
            const col = Math.floor(rand() * cols);
            // Don't place wall at start position
            if (!(row === rows - 1 && col === 0)) {
                walls[row][col] = 1;
            }
        }
    };

    // Generate challenging daily maze with varied dimensions and complexity
    const generateHiddenMaze = useCallback(() => {
        const seed = getDailySeed();

        // Simple hash function for seed
        let hashCode = 0;
        for (let i = 0; i < seed.length; i++) {
            hashCode = seed.charCodeAt(i) + ((hashCode << 5) - hashCode);
        }

        // Create seeded random function
        let seedValue = Math.abs(hashCode);
        const seededRand = () => {
            seedValue = (seedValue * 9301 + 49297) % 233280;
            return seedValue / 233280;
        };

        // Generate variable grid size for more challenge (3x3, 4x3, 3x4, 4x4, 5x3, 3x5)
        const gridOptions = [
            { rows: 3, cols: 3 }, // Easy
            { rows: 4, cols: 3 }, // Medium
            { rows: 3, cols: 4 }, // Medium
            { rows: 4, cols: 4 }, // Hard
            { rows: 5, cols: 3 }, // Hard
            { rows: 3, cols: 5 }, // Hard
            { rows: 5, cols: 4 }, // Very Hard
            { rows: 4, cols: 5 }  // Very Hard
        ];

        const selectedGrid = gridOptions[Math.floor(seededRand() * gridOptions.length)];
        const { rows, cols } = selectedGrid;

        // Create grid-based walls with more strategic patterns
        const walls = Array(rows).fill().map(() => Array(cols).fill(0));

        // Different maze pattern types based on seed
        const patternType = Math.floor(seededRand() * 5);

        switch (patternType) {
            case 0: // Spiral pattern
                createSpiralWalls(walls, rows, cols, seededRand);
                break;
            case 1: // Cross pattern
                createCrossWalls(walls, rows, cols, seededRand);
                break;
            case 2: // Diagonal barriers
                createDiagonalWalls(walls, rows, cols, seededRand);
                break;
            case 3: // Corner traps
                createCornerWalls(walls, rows, cols, seededRand);
                break;
            default: // Random scattered
                createRandomWalls(walls, rows, cols, seededRand);
        }

        // Generate available positions (excluding start position and walls)
        const startRow = rows - 1;
        const startCol = 0;
        const availablePositions = [];

        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                if (!(row === startRow && col === startCol) && walls[row][col] === 0) {
                    availablePositions.push({ row, col });
                }
            }
        }

        // Shuffle available positions
        for (let i = availablePositions.length - 1; i > 0; i--) {
            const j = Math.floor(seededRand() * (i + 1));
            [availablePositions[i], availablePositions[j]] = [availablePositions[j], availablePositions[i]];
        }

        // Generate keys based on grid complexity (more keys for larger grids)
        const totalCells = rows * cols;
        const keyCount = Math.min(
            Math.floor(seededRand() * Math.max(2, Math.floor(totalCells / 6))) + 1,
            Math.max(1, Math.floor(availablePositions.length * 0.4))
        );

        const keys = [];
        for (let i = 0; i < Math.min(keyCount, availablePositions.length - 1); i++) {
            keys.push(availablePositions[i]);
        }

        // Place door at strategic position (prefer corners or edges for challenge)
        let door;
        const remainingPositions = availablePositions.slice(keys.length);
        const cornerPositions = remainingPositions.filter(pos =>
            (pos.row === 0 || pos.row === rows - 1) &&
            (pos.col === 0 || pos.col === cols - 1)
        );

        if (cornerPositions.length > 0) {
            door = cornerPositions[Math.floor(seededRand() * cornerPositions.length)];
        } else {
            door = remainingPositions[0] || { row: 0, col: cols - 1 };
        }

        return {
            id: Math.floor(seededRand() * 1000) + 1,
            walls,
            keys,
            door,
            rows,
            cols
        };
    }, [getDailySeed]); // Add dependencies

    // Initialize game
    useEffect(() => {
        const maze = generateHiddenMaze();
        setGameState(maze);
        const startRow = maze.rows - 1;
        const startCol = 0;
        setPlayerPosition({ row: startRow, col: startCol });
        setCollectedKeys([]);
        setVisitedCells(new Set([`${startRow},${startCol}`]));

        // Load streak from localStorage
        const savedData = JSON.parse(localStorage.getItem(`hiddenmaze-${pillarName}`) || '{}');
        setStreak(savedData.streak || 0);
    }, [pillarName, generateHiddenMaze]);

    // Update streak with proper daily tracking
    const updateStreak = useCallback(() => {
        const today = new Date().toDateString();
        const savedData = JSON.parse(localStorage.getItem(`hiddenmaze-${pillarName}`) || '{}');

        // If already completed today, don't update streak
        if (savedData.lastPlayed === today) {
            setStreak(savedData.streak || 1);
            return;
        }

        let newStreak = 1;
        if (savedData.lastPlayed) {
            const lastDate = new Date(savedData.lastPlayed);
            const todayDate = new Date();

            // Calculate days difference properly
            lastDate.setHours(0, 0, 0, 0);
            todayDate.setHours(0, 0, 0, 0);
            const daysDiff = Math.floor((todayDate - lastDate) / (1000 * 60 * 60 * 24));

            if (daysDiff === 1) {
                // Consecutive day - increment streak
                newStreak = (savedData.streak || 0) + 1;
            } else if (daysDiff > 1) {
                // Gap in days - reset streak
                newStreak = 1;
            }
        }

        setStreak(newStreak);
        localStorage.setItem(`hiddenmaze-${pillarName}`, JSON.stringify({
            streak: newStreak,
            lastPlayed: today
        }));
    }, [pillarName]); // Add dependencies

    // Move player function
    const movePlayer = useCallback((newPosition) => {
        if (!gameState || isComplete) return;

        // Check if new position has a wall
        if (gameState.walls[newPosition.row][newPosition.col] === 1) {
            // Hit wall - flash red and reset everything
            setHitWall(true);
            const startRow = gameState.rows - 1;
            const startCol = 0;
            setPlayerPosition({ row: startRow, col: startCol });
            setCollectedKeys([]); // Clear all collected keys - start fresh
            setVisitedCells(new Set([`${startRow},${startCol}`]));
            setMessage('Hit a wall! Keys lost. Start over!');

            setTimeout(() => {
                setHitWall(false);
                setMessage('');
            }, 2000);
            return;
        }

        // Valid move - update position
        setPlayerPosition(newPosition);
        setVisitedCells(prev => new Set([...prev, `${newPosition.row},${newPosition.col}`]));

        // Check if player collected a key FIRST (before door checks)
        let newCollectedKeys = [...collectedKeys];
        gameState.keys.forEach(key => {
            if (key.row === newPosition.row && key.col === newPosition.col) {
                if (!collectedKeys.some(k => k.row === key.row && k.col === key.col)) {
                    newCollectedKeys = [...newCollectedKeys, key];
                    setCollectedKeys(newCollectedKeys);
                    setMessage('Key collected! 🗝️');
                    setTimeout(() => setMessage(''), 1500);
                }
            }
        });

        // Now check door logic with updated key count
        if (gameState.door.row === newPosition.row && gameState.door.col === newPosition.col) {
            if (newCollectedKeys.length < gameState.keys.length) {
                // Hit blocked door - reset position AND clear collected keys
                setHitWall(true);
                const startRow = gameState.rows - 1;
                const startCol = 0;
                setPlayerPosition({ row: startRow, col: startCol });
                setCollectedKeys([]); // Clear all collected keys - start fresh
                setVisitedCells(new Set([`${startRow},${startCol}`]));
                setMessage(`Blocked door! Keys lost. Collect all ${gameState.keys.length} keys again!`);

                setTimeout(() => {
                    setHitWall(false);
                    setMessage('');
                }, 2000);
                return;
            } else {
                // All keys collected - complete the maze
                setIsComplete(true);
                updateStreak();
                setMessage(`Maze completed in ${formatTime(timeElapsed)}! 🎉`);
            }
        }
    }, [gameState, isComplete, collectedKeys, timeElapsed, updateStreak]); // Add dependencies

    // Handle keyboard movement
    useEffect(() => {
        const handleKeyPress = (e) => {
            if (isComplete) return;

            if (!gameStarted) {
                setGameStarted(true);
            }

            let newPosition = { ...playerPosition };

            switch (e.key.toLowerCase()) {
                case 'w':
                case 'arrowup':
                    newPosition.row = Math.max(0, playerPosition.row - 1);
                    break;
                case 's':
                case 'arrowdown':
                    newPosition.row = Math.min(gameState?.rows - 1, playerPosition.row + 1);
                    break;
                case 'a':
                case 'arrowleft':
                    newPosition.col = Math.max(0, playerPosition.col - 1);
                    break;
                case 'd':
                case 'arrowright':
                    newPosition.col = Math.min(gameState?.cols - 1, playerPosition.col + 1);
                    break;
                default:
                    return;
            }

            e.preventDefault();
            movePlayer(newPosition);
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [playerPosition, gameState, isComplete, gameStarted, movePlayer]);

    // Reset maze
    const resetMaze = () => {
        if (!gameState) return;
        const startRow = gameState.rows - 1;
        const startCol = 0;
        setPlayerPosition({ row: startRow, col: startCol });
        setCollectedKeys([]);
        setVisitedCells(new Set([`${startRow},${startCol}`]));
        setIsComplete(false);
        setTimeElapsed(0); // Reset stopwatch
        setGameStarted(false);
        setMessage('');
        setHitWall(false);
    };

    if (!gameState) {
        return (
            <div className="doorkey-overlay" onClick={onClose}>
                <div className="doorkey-modal">
                    <div className="doorkey-loading">Loading maze...</div>
                </div>
            </div>
        );
    }

    return (
        <div className="doorkey-overlay" onClick={onClose}>
            <motion.div
                className={`doorkey-modal ${hitWall ? 'wall-hit' : ''}`}
                onClick={(e) => e.stopPropagation()}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
            >
                {/* Header */}
                <div className="doorkey-header">
                    <div className="doorkey-title">
                        <Key size={24} />
                        <h2>Hidden Maze Challenge - {pillarName}</h2>
                    </div>
                    <button className="doorkey-close" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                {/* Stats & Timer */}
                <div className="doorkey-stats">
                    <div className="doorkey-stat">
                        <Calendar size={20} />
                        <span>Today's Challenge</span>
                    </div>
                    <div className="doorkey-stat doorkey-stat--streak">
                        <Flame size={20} />
                        <span>{streak} Day Streak</span>
                    </div>
                    <div className="doorkey-stat doorkey-stat--timer">
                        <Clock size={20} />
                        <span>{formatTime(timeElapsed)}</span>
                    </div>
                    <button
                        className="doorkey-rules-btn"
                        onClick={() => setShowRules(!showRules)}
                    >
                        <HelpCircle size={20} />
                        <span>Rules</span>
                    </button>
                </div>

                {/* Rules */}
                <AnimatePresence>
                    {showRules && (
                        <motion.div
                            className="doorkey-rules"
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                        >
                            <h3>🧩 How to Play:</h3>
                            <ul>
                                <li><strong>Dynamic hidden maze:</strong> Daily changing maze sizes and patterns</li>
                                <li><strong>Movement:</strong> Use Arrow keys or WASD to move</li>
                                <li><strong>Collect keys:</strong> Find all keys hidden in the maze</li>
                                <li><strong>Reach the door:</strong> Only accessible after collecting all keys</li>
                                <li><strong>Wall penalty:</strong> Hitting a wall resets you to start</li>
                                <li><strong>Path tracking:</strong> Your path turns dark to help navigation</li>
                                <li><strong>Daily challenge:</strong> New maze patterns generated each day</li>
                                <li><strong>Time limit:</strong> You have 3 minutes per round</li>
                            </ul>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Game Status */}
                <div className="maze-status">
                    <div className="status-item">
                        <Key size={16} />
                        <span>Keys: {collectedKeys.length}/{gameState.keys.length}</span>
                    </div>
                    {message && (
                        <div className="status-message">{message}</div>
                    )}
                </div>

                {/* Dynamic Maze Grid */}
                <div
                    className="maze-grid"
                    style={{
                        gridTemplateColumns: `repeat(${gameState.cols}, 1fr)`,
                        gridTemplateRows: `repeat(${gameState.rows}, 1fr)`
                    }}
                >
                    {Array.from({ length: gameState.rows }, (_, row) =>
                        Array.from({ length: gameState.cols }, (_, col) => {
                            const isPlayer = playerPosition.row === row && playerPosition.col === col;
                            const isKey = gameState.keys.some(key => key.row === row && key.col === col &&
                                !collectedKeys.some(ck => ck.row === key.row && ck.col === key.col));
                            const isDoor = gameState.door.row === row && gameState.door.col === col;
                            const isVisited = visitedCells.has(`${row},${col}`);
                            const canOpenDoor = isDoor && collectedKeys.length === gameState.keys.length;
                            const isLockedDoor = isDoor && collectedKeys.length < gameState.keys.length;

                            let cellClasses = `maze-cell ${isVisited ? 'visited' : ''}`;
                            if (canOpenDoor) cellClasses += ' door-unlocked';
                            if (isLockedDoor) cellClasses += ' door-locked';

                            return (
                                <div
                                    key={`${row}-${col}`}
                                    className={cellClasses}
                                    onClick={() => movePlayer({ row, col })}
                                >
                                    {isPlayer && (
                                        <User size={24} className="player-icon" />
                                    )}
                                    {isKey && (
                                        <Key size={20} className="key-icon" />
                                    )}
                                    {isDoor && (
                                        <DoorOpen
                                            size={24}
                                            className={`door-icon ${canOpenDoor ? 'unlocked' : 'locked'}`}
                                            style={{
                                                color: canOpenDoor ? '#22c55e' : '#ef4444'
                                            }}
                                        />
                                    )}
                                </div>
                            );
                        })
                    )}
                </div>

                {/* Instructions */}
                <div className="maze-instructions">
                    <p>
                        Collect <strong>{gameState.keys.length} KEY{gameState.keys.length > 1 ? 'S' : ''}</strong> then get to the <strong>DOOR</strong>
                    </p>
                    <p className="controls-hint">
                        Use ←→↑↓ or WASD to move
                    </p>
                </div>

                {/* Success Message */}
                <AnimatePresence>
                    {isComplete && (
                        <motion.div
                            className="doorkey-success-overlay"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <motion.div
                                className="doorkey-success-popup"
                                initial={{ opacity: 0, scale: 0.8, y: 20 }}
                                animate={{ opacity: 1, scale: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.8, y: 20 }}
                            >
                                <Trophy size={64} />
                                <h3>Maze Complete! 🎉</h3>
                                <p className="completion-time">Completed in: <strong>{formatTime(timeElapsed)}</strong></p>
                                <p className="streak-info">Your streak: <strong>{streak} days</strong></p>
                                <p className="next-challenge">Come back tomorrow for a new challenge!</p>
                                <button className="doorkey-btn doorkey-btn--primary" onClick={onClose}>
                                    Close
                                </button>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Actions */}
                <div className="doorkey-actions">
                    <button className="doorkey-btn doorkey-btn--secondary" onClick={resetMaze}>
                        <RefreshCw size={18} />
                        Reset
                    </button>
                </div>
            </motion.div>
        </div>
    );
};

export default DoorKeyGame;