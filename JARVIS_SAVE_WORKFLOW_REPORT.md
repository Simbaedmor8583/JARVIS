# JARVIS Save Workflow Report

Date: 2026-07-20

## Flow

1. A completed document creates `PendingSaveRequest`.
2. JARVIS asks where to save.
3. Known folders, absolute paths, nested known-folder paths, and the JARVIS `.test_tmp` alias are resolved.
4. JARVIS states the exact full path.
5. Folder creation and overwrite effects are disclosed.
6. Save occurs only after `Yes`.
7. The file is verified on disk.

## Live Result

- Location phrase: `Save it in the JARVIS .test_tmp folder.`
- Confirmed path: `.test_tmp\Renewable Energy Report.docx`.
- Confirmation response: saved and verified.
- File exists: yes.
- Reopened with `python-docx`: yes.
- Paragraphs: 15.
- References: 4 URLs.
- Save failure handling clears the unsafe pending state and never claims success.

## Safety

- No unknown default location is used.
- Existing-file overwrite is disclosed before save.
- Missing destination folder creation is disclosed before save.
- Filenames remove Windows-invalid characters.

