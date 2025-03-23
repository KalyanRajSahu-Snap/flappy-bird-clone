# Flappy Bird Clone

A responsive, feature-complete Flappy Bird clone built with React and TypeScript. This project recreates the classic mobile game with authentic visuals, sounds, and gameplay mechanics.

## Features

- **Classic Gameplay**: Jump through pipes and try to achieve the highest score
- **Original Graphics**: Authentic sprites and animations from the original game
- **Sound Effects**: Original sound effects for jump, scoring, and collisions
- **Responsive Design**: Play on desktop or mobile devices
- **Mobile Support**: Tap to jump on touch devices
- **Game States**: Start screen, gameplay, and game over screens

## Technologies Used

- React.js
- TypeScript
- HTML Canvas API
- Next.js

## Installation

### Prerequisites

- Node.js (v14.0.0 or higher)
- npm or yarn

### Clone the Repository

```bash
git clone https://github.com/KalyanRajSahu-Snap/flappy-bird-clone.git
cd flappy-bird-clone
```

### Install Dependencies

```bash
npm install
# or
yarn install
```

### Run Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the game.

## How to Play

- **Start the game**: Press space bar or click/tap the game area
- **Jump**: Press space bar or click/tap the game area during gameplay
- **Restart**: Click the restart button after game over

## Project Structure

- `FlappyBird.tsx` - Main game component containing game logic and rendering
- Assets are loaded from a Vercel Blob Storage for optimal performance

## Game Logic

The game implements the following core mechanics:

- Gravity and jumping physics
- Procedurally generated pipes with random heights
- Collision detection between the bird and pipes
- Score tracking and display
- Animation states for the bird

## Customization

You can customize the game by modifying the constants at the top of the file:

```typescript
const GRAVITY = 0.5
const JUMP_STRENGTH = 10
const PIPE_WIDTH = 52
const PIPE_GAP = 150
const PIPE_SPEED = 2
const BIRD_WIDTH = 34
const BIRD_HEIGHT = 24
```

## Deployment

This project can be easily deployed to Vercel:

```bash
npm run build
# or
yarn build
```

## Credits

- Original Flappy Bird game created by Dong Nguyen
- Sprites and audio are used for educational purposes

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
