import { createFileRoute, createLazyFileRoute } from '@tanstack/react-router'
import { Chessboard } from 'react-chessboard'

export const Route = createFileRoute('/game/')({
  component: About,
})

function About() {
  return <div className="p-2 w-[500px]">
    <Chessboard id="BasicBoard" 
    onPieceDrop={(from, to,piece) => {
      console.log(from, to, piece)
        return true 
    }}
    />
  </div>
} 