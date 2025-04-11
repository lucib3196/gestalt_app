"use client";
import React, { useEffect, useState } from "react";
import api from "@/api";
import { useParams } from "next/navigation";

import { useRouter } from "next/navigation";


interface FileResponse {
  id: number;
  name: string;
  content: string;
  // save_name: string | null;
  folder_id: number;
};

















export default function page() {
  return (
    <div>All Files</div>
  )
}
