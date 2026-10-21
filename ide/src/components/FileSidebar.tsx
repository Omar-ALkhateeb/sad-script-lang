// ide/src/components/FileSidebar.tsx
import React, { useState, useRef } from "react";
import {
  FileCode,
  FileSpreadsheet,
  Folder,
  FolderOpen,
  FolderPlus,
  FilePlus,
  Upload,
  Trash2,
  Pencil,
  ChevronDown,
  ChevronLeft,
} from "lucide-react";
import { VirtualFile } from "../types/ide";

interface FileSidebarProps {
  files: VirtualFile[];
  activeFileName: string;
  onSelectFile: (name: string) => void;
  onCreateFile: (name: string, type: "sad" | "csv", content?: string) => void;
  onRenameFile: (oldName: string, newName: string) => void;
  onDeleteFile: (name: string) => void;
}

export const FileSidebar: React.FC<FileSidebarProps> = ({
  files,
  activeFileName,
  onSelectFile,
  onCreateFile,
  onRenameFile,
  onDeleteFile,
}) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [rootExpanded, setRootExpanded] = useState<boolean>(true);
  const [folders, setFolders] = useState<string[]>([]);
  const [collapsedFolders, setCollapsedFolders] = useState<
    Record<string, boolean>
  >({});
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);

  const [creatingMode, setCreatingMode] = useState<
    "sad" | "csv" | "folder" | null
  >(null);
  const [inlineInputVal, setInlineInputVal] = useState<string>("");

  const [renamingFile, setRenamingFile] = useState<string | null>(null);
  const [renameVal, setRenameVal] = useState<string>("");
  const [isDraggingOver, setIsDraggingOver] = useState<boolean>(false);

  const allFolders = Array.from(
    new Set([
      ...folders,
      ...files
        .filter((f) => f.name.includes("/"))
        .map((f) => f.name.split("/")[0]),
    ]),
  );

  const startCreating = (
    e: React.MouseEvent,
    mode: "sad" | "csv" | "folder",
  ) => {
    e.stopPropagation();
    setRootExpanded(true);
    setCreatingMode(mode);
    const prefix = selectedFolder ? `${selectedFolder}/` : "";
    if (mode === "sad")
      setInlineInputVal(`${prefix}script_${files.length + 1}.sad`);
    else if (mode === "csv")
      setInlineInputVal(`${prefix}data_${files.length + 1}.csv`);
    else setInlineInputVal("مجلد");
  };

  const commitInlineCreate = () => {
    const raw = inlineInputVal.trim();
    if (!raw || !creatingMode) {
      setCreatingMode(null);
      return;
    }

    if (creatingMode === "folder") {
      const cleanFolder = raw.replace(/\//g, "");
      if (cleanFolder && !allFolders.includes(cleanFolder)) {
        setFolders((prev) => [...prev, cleanFolder]);
      }
      setSelectedFolder(cleanFolder);
    } else {
      const ext = creatingMode === "csv" ? ".csv" : ".sad";
      const finalName = raw.endsWith(ext) ? raw : `${raw}${ext}`;
      const starter =
        creatingMode === "csv"
          ? "الاسم,الدرجة\nأحمد,95\nسارة,98"
          : '// ملف برمجي جديد\nاطبع("مرحباً!")\n';
      onCreateFile(finalName, creatingMode, starter);
    }
    setCreatingMode(null);
    setInlineInputVal("");
  };

  const commitRename = (oldName: string) => {
    const trimmed = renameVal.trim();
    if (trimmed && trimmed !== oldName) {
      onRenameFile(oldName, trimmed);
    }
    setRenamingFile(null);
  };

  const handleUploadFiles = async (fileList: FileList | null) => {
    if (!fileList) return;
    for (const file of Array.from(fileList)) {
      const text = await file.text();
      const isCsv = file.name.toLowerCase().endsWith(".csv");
      const targetPath = selectedFolder
        ? `${selectedFolder}/${file.name}`
        : file.name;
      onCreateFile(targetPath, isCsv ? "csv" : "sad", text);
    }
  };

  const renderFileRow = (file: VirtualFile, depth = 1) => {
    const isActive = file.name === activeFileName;
    const displayName = file.name.includes("/")
      ? file.name.split("/").slice(1).join("/")
      : file.name;
    const paddingRight = depth === 1 ? "pr-5" : "pr-9";

    if (renamingFile === file.name) {
      return (
        <div key={file.name} className={`${paddingRight} pl-2 py-0.5`}>
          <input
            autoFocus
            value={renameVal}
            onChange={(e) => setRenameVal(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") commitRename(file.name);
              if (e.key === "Escape") setRenamingFile(null);
            }}
            onBlur={() => commitRename(file.name)}
            dir="ltr"
            className="w-full bg-[var(--sol-base3)] text-[var(--sol-base01)] text-xs px-1.5 py-0.5 border border-[var(--sol-blue)] outline-none font-mono"
          />
        </div>
      );
    }

    return (
      <div
        key={file.name}
        onClick={() => onSelectFile(file.name)}
        onDoubleClick={() => {
          setRenamingFile(file.name);
          setRenameVal(file.name);
        }}
        className={`group h-[24px] flex items-center justify-between ${paddingRight} pl-2 text-xs cursor-pointer transition-colors ${
          isActive
            ? "bg-[#e1dbcd] text-[var(--sol-base01)] font-semibold"
            : "text-[var(--sol-base00)] hover:bg-[#e6e0d2]"
        }`}
      >
        <div className="flex items-center gap-1.5 truncate">
          {file.type === "csv" ? (
            <FileSpreadsheet className="w-3.5 h-3.5 text-[var(--sol-green)] shrink-0" />
          ) : (
            <FileCode className="w-3.5 h-3.5 text-[var(--sol-blue)] shrink-0" />
          )}
          <span className="truncate font-mono text-[12px]" dir="ltr">
            {displayName}
          </span>
        </div>

        <div className="opacity-0 group-hover:opacity-100 flex items-center gap-1">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setRenamingFile(file.name);
              setRenameVal(file.name);
            }}
            className="text-[var(--sol-base1)] hover:text-[var(--sol-base01)] cursor-pointer"
            title="إعادة تسمية"
          >
            <Pencil className="w-3 h-3" />
          </button>
          {files.length > 1 && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteFile(file.name);
              }}
              className="text-[var(--sol-base1)] hover:text-[var(--sol-red)] cursor-pointer"
              title="حذف"
            >
              <Trash2 className="w-3 h-3" />
            </button>
          )}
        </div>
      </div>
    );
  };

  const rootFiles = files.filter((f) => !f.name.includes("/"));

  return (
    <aside
      onDragOver={(e) => {
        e.preventDefault();
        setIsDraggingOver(true);
      }}
      onDragLeave={() => setIsDraggingOver(false)}
      onDrop={async (e) => {
        e.preventDefault();
        setIsDraggingOver(false);
        await handleUploadFiles(e.dataTransfer.files);
      }}
      className="h-full bg-[var(--sol-base2)] flex flex-col select-none relative overflow-hidden"
    >
      {isDraggingOver && (
        <div className="absolute inset-0 z-30 bg-[var(--sol-base3)]/90 border-2 border-dashed border-[var(--sol-blue)] flex flex-col items-center justify-center p-4 text-center">
          <Upload className="w-6 h-6 text-[var(--sol-blue)] mb-1" />
          <span className="text-xs font-bold text-[var(--sol-base01)]">
            أفلت الملفات هنا لإضافتها
          </span>
        </div>
      )}

      {/* VS Code Collapsible Project Header with Hover-Only Action Icons */}
      <div
        onClick={() => setRootExpanded(!rootExpanded)}
        className="group h-7 px-2 flex items-center justify-between border-b border-[var(--sol-border)] cursor-pointer hover:bg-[#e6e0d2]"
      >
        <div className="flex items-center gap-1 text-[11px] font-bold text-[var(--sol-base01)]">
          {rootExpanded ? (
            <ChevronDown className="w-3.5 h-3.5" />
          ) : (
            <ChevronLeft className="w-3.5 h-3.5" />
          )}
          <span>المشروع (sad)</span>
        </div>

        {/* Action Icons (Visible on hover, just like VS Code) */}
        <div className="opacity-80 group-hover:opacity-100 flex items-center gap-1">
          <button
            type="button"
            onClick={(e) => startCreating(e, "sad")}
            title="ملف جديد"
            className="p-0.5 rounded hover:bg-[#d8d2c1] text-[var(--sol-base01)] cursor-pointer"
          >
            <FilePlus className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={(e) => startCreating(e, "folder")}
            title="مجلد جديد"
            className="p-0.5 rounded hover:bg-[#d8d2c1] text-[var(--sol-base01)] cursor-pointer"
          >
            <FolderPlus className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              fileInputRef.current?.click();
            }}
            title="رفع ملف (.csv أو .sad)"
            className="p-0.5 rounded hover:bg-[#d8d2c1] text-[var(--sol-base01)] cursor-pointer"
          >
            <Upload className="w-3.5 h-3.5" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.sad,.txt"
            multiple
            onChange={(e) => {
              handleUploadFiles(e.target.files);
              e.target.value = "";
            }}
            className="hidden"
          />
        </div>
      </div>

      {/* Inline File/Folder Input Row */}
      {creatingMode && (
        <div className="pr-5 pl-2 py-1 bg-[#e6e0d2]">
          <input
            autoFocus
            value={inlineInputVal}
            onChange={(e) => setInlineInputVal(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") commitInlineCreate();
              if (e.key === "Escape") setCreatingMode(null);
            }}
            onBlur={commitInlineCreate}
            dir="ltr"
            placeholder={
              creatingMode === "folder" ? "اسم المجلد..." : "filename.sad"
            }
            className="w-full bg-[var(--sol-base3)] text-[var(--sol-base01)] text-xs px-1.5 py-0.5 border border-[var(--sol-blue)] outline-none font-mono"
          />
        </div>
      )}

      {/* Flat VS Code File Tree */}
      {rootExpanded && (
        <div className="flex-1 overflow-y-auto py-0.5">
          {allFolders.map((folderName) => {
            const isCollapsed = Boolean(collapsedFolders[folderName]);
            const isSelected = selectedFolder === folderName;
            const folderFiles = files.filter((f) =>
              f.name.startsWith(`${folderName}/`),
            );

            return (
              <div key={folderName}>
                <div
                  onClick={() => {
                    setSelectedFolder((prev) =>
                      prev === folderName ? null : folderName,
                    );
                    setCollapsedFolders((prev) => ({
                      ...prev,
                      [folderName]: !prev[folderName],
                    }));
                  }}
                  className={`h-[24px] pr-3 pl-2 flex items-center gap-1 text-xs cursor-pointer ${
                    isSelected
                      ? "bg-[#e1dbcd] text-[var(--sol-base01)] font-semibold"
                      : "text-[var(--sol-base00)] hover:bg-[#e6e0d2]"
                  }`}
                >
                  {isCollapsed ? (
                    <ChevronLeft className="w-3.5 h-3.5 text-[var(--sol-base1)] shrink-0" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-[var(--sol-base1)] shrink-0" />
                  )}
                  {isCollapsed ? (
                    <Folder className="w-3.5 h-3.5 text-[var(--sol-yellow)] shrink-0" />
                  ) : (
                    <FolderOpen className="w-3.5 h-3.5 text-[var(--sol-yellow)] shrink-0" />
                  )}
                  <span className="truncate">{folderName}</span>
                </div>

                {!isCollapsed && (
                  <div className="border-r border-[var(--sol-border)] mr-4">
                    {folderFiles.map((f) => renderFileRow(f, 2))}
                  </div>
                )}
              </div>
            );
          })}

          {rootFiles.map((file) => renderFileRow(file, 1))}
        </div>
      )}
    </aside>
  );
};
