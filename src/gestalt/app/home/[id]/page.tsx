'use client'; 

import { useParams } from 'next/navigation';

export default function HomePersonal() {
  const params = useParams();
  const id = params.id;

  return <h1>Hi {id}</h1>;
}
