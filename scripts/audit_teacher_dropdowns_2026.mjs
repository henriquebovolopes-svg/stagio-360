#!/usr/bin/env node
/* Auditoria 2026: seleção completa de professores sem vincular identidades não homologadas. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const checks={
 'admin/planejamento.html':[
  'function loadTeacherRoster()',
  "source_module','M1'",
  'stg_360_coord_fiiem_items',
  'stg_360_survey_teacher_blocks',
  'stg_360_teacher_registry_pending',
  'teacherRoster.find',
  'teacher-roster-note',
  'Com planejamentos registrados',
  'Demais referências docentes no ciclo',
  "selectedTeacher?.kind==='planning'",
  'Nenhuma aula foi atribuída por semelhança de nome.',
  'await loadTeacherRoster()'
 ],
 'admin/coord-fii-em.html':[
  'function teacherChoices()',
  'stg_360_survey_teacher_blocks',
  'source_teacher_id',
  "id:'student:'+b.cohort+':'+b.block_number",
  "const isStudentOnly=teacher.startsWith('student:')",
  'Nenhuma nota foi atribuída automaticamente.',
  "if(key==='stage')teacherChoices()"
 ],
 'admin/pdi.html':[
  'Profissional do ciclo M1/2026',
  "eq('source_module','M1')",
  "if(!data?.length)",
  "selected?.scope==='REGENTE CONFIRMADA'",
  "selected.scope!=='REGENTE CONFIRMADA'",
  'Demais profissionais do ciclo · consulta individual'
 ],
 'admin/sintese.html':[
  '<option value="todos">Todos os profissionais do ciclo M1/2026</option>',
  'Selecionar profissional do ciclo',
  "scopeTeachers.forEach(t=>"
 ],
 'admin/pesquisas-2026.html':[
  'Professor do ciclo M1/2026',
  'function teacherOptions()',
  "b.cohort+'|'+b.block_number",
  'x.teacherKey===teacher',
  'block_number,first_source_column',
  'teacherOptions();limit=70;render()'
 ],
 'admin/index.html':[
  "sup.from('stg_teachers').select('id,name,classes,scope,role_label')",
  "addSelect($('erica-select'),teacherList.map"
 ]
};
let errors=[];
const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'stagio-teacher-modules-'));
try {
 for(const [file,tokens] of Object.entries(checks)){
  const html=fs.readFileSync(file,'utf8');
  for(const token of tokens)if(!html.includes(token))errors.push(file+': requisito ausente: '+token);
  const scripts=[...html.matchAll(/<script\b[^>]*type=["']module["'][^>]*>([\s\S]*?)<\/script>/gi)];
  if(!scripts.length){errors.push(file+': módulo JavaScript ausente');continue}
  for(let i=0;i<scripts.length;i++){
   const tmp=path.join(temporary,path.basename(file,'.html')+'-'+i+'.mjs');
   fs.writeFileSync(tmp,scripts[i][1],'utf8');
   try{execFileSync(process.execPath,['--check',tmp],{stdio:'pipe'})}
   catch(error){errors.push(file+': erro de sintaxe JavaScript: '+String(error.stderr||error.message).slice(0,400))}
  }
 }
} finally {fs.rmSync(temporary,{recursive:true,force:true})}
console.log('Auditoria de listas docentes M1/2026: '+Object.keys(checks).length+' páginas, '+errors.length+' erro(s).');
for(const issue of errors)console.error('ERRO:',issue);
if(errors.length)process.exit(1);
