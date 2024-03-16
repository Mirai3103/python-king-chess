import { createFileRoute } from '@tanstack/react-router'
import { Chessboard } from 'react-chessboard'
import React from 'react'
export const Route = createFileRoute('/game/')({
  component: About,
})

function About() {

 
  return <div className="p-2 w-[500px]">
    <Chessboard id="BasicBoard"
      onPieceDrop={(from, to, piece) => {
        console.log(from, to, piece)
        return true
      }}
    />
    <button  className="bg-blue-500 text-white p-2 rounded-md">
      Create Game
    </button>
  </div>
} 