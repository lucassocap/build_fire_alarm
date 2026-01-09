# Extracted Content: PE fire-alarm workflow.pdf

**Total Pages**: 6


## Page 1

Florida  PE  Fire  Alarm  Workflow  to  Web  
App
 
Architecture
 
This  document  details  the  professional  engineering  PE  fire-alarm  design  workflow  for  
Florida
 
projects
 
and
 
outlines
 
how
 
to
 
translate
 
this
 
process
 
into
 
a
 
web
 
application
 
that
 
generates
 
a
 
detailed
 
Bill
 
of
 
Materials
 
BOM
 
and
 
code-compliance
 
notes,
 
cross-referenced
 
to
 
Kidde
 
Commercial
 
products.
  The  core  goal  is  to  ingest  project  attributes  and  output  a  detailed  BOM  plus  
code-compliance
 
check
 
notes
,
 
and
 
then
 
cross-reference
 
that
 
BOM
 
to
 
Kidde
 
Commercial
 
equivalents,
 
w i t h o u t 
 
performing
 
drawing
 
or
 
device
 
placement.
 
A  Florida  PE  Fire  Alarm  Design  Workflow  
The  professional  design  process  is  structured  into  three  phases  to  establish  the  code  
basis,
 
system
 
scope,
 
and
 
final
 
BOM.
 
Phase  1  —  Architectural  Plan  Review  System  Scoping)  This  phase  establishes  the  code  basis  and  system  scope  by  extracting  key  project  data  
from
 
architectural
 
sets.
 
Project  Identity  and  Jurisdiction  
Input  Requirement  
Project  Location  Project  address,  city/county  
Authorities  Having  Jurisdiction  AHJ  Fire  Marshal,  Building  Dept.  
Code  Enforcement  Florida  Building  Code  FBC  plan  review  +  Florida  Fire  Prevention  Code  FFPC  enforcement  
Local  Factors  High-rise  triggers,  local  amendments,  special  districts  

---

## Page 2

Occupancy  /  Use  Classification  System  Requirement  Driver)  Classification  determines  if  a  system  is  required  and  its  type  (manual,  automatic  
detection,
 
voice/EVACS.
  ●  Primary  Occupancy:  Business,  Mercantile,  Storage,  Factory/Industrial,  
Residential/Multi-family.
 ●  Mixed-Use:  Separations  and  accessory  uses  (e.g.,  retail  under  residential).  ●  Special  Rooms:  Electrical  rooms,  fire  pump  room,  generator,  elevator  machine  
room,
 
commercial
 
kitchen
 
hood,
 
hazmat.
 
Size  and  Geometry  Notification  Scope  Driver)  These  inputs  drive  the  conceptual  sizing  of  the  system  components  BOM-level  scope).   ●  Total  building  area,  floor  areas,  number  of  stories.  ●  Ceiling  heights  and  types  (open  structure  vs.  ACT.  ●  Egress/Life  Safety  Features:  Rated  corridors,  exit  access  corridors,  stairs.  
Egress  and  Life  Safety  Features  Interfaces)  These  details  define  the  interface  scope  for  the  fire  alarm  control  panel  FACP.   ●  Elevator  count  and  recall  requirements  (smoke  detector  locations  for  recall/shunt  
trip).
 ●  Door  hardware  schedules  for  maglocks  /  access  control  (unlocking  interfaces).  ●  HVAC  shutdown  zoning  concept.  ●  Sprinkler  system  presence  (for  annunciation  and  location  text).   Output  of  Phase  1  Structured  "Project  Intake  Record"  Occupancy,  Floors,  Areas,  
Interfaces,
 
Design
 
Basis
 
Assumptions).
 
Phase  2  —  Code  Research  and  Application  Design  Basis)  The  design  must  comply  with  two  primary  "code  umbrellas"  in  Florida,  plus  referenced  
standards
 
and
 
state
 
engineering
 
rules.
  1.  Florida  Fire  Prevention  Code  FFPC  Enforced  by  local  fire  officials.  References  
NFPA
 
1
 
/
 
NFPA
 
101.
 2.  Florida  Building  Code  FBC  Design  framework  for  permitting.  Specifically  FBC  
Building
 
and
 
FBC
 
Fire
 
Protection
 
Systems.
  The  design  is  engineered  according  to  the  following  referenced  standards:   

---

## Page 3

●  NFPA  72  The  h o w - t o  standard  for  design,  installation,  and  performance.  ●  NFPA  101  Often  governs  egress  and  occupant  notification  intent.  ●  NEC  /  NFPA  70  Affects  wiring  methods,  power,  and  pathway  survivability.  
Code  Methodology  App  Thinking  Model)  1.  Determine  IF  a  system  is  required  FBC/FFPC.  2.  Determine  WHAT  TYPE  is  required  Manual  only,  automatic  detection,  voice,  
monitoring).
 3.  Determine  PERFORMANCE  RULES  Audibility,  intelligibility,  candela  rules,  
survivability)
 
via
 
NFPA
 
72.
 4.  Determine  DOCUMENTATION  RULES  for  submittal  per  Florida  engineering  rules  
FAC
 
61G1532.
 
Phase  3  —  Design  Implementation  BOM  +  Compliance  Notes)  The  scope  is  translated  into  a  category-based  Bill  of  Materials  and  supporting  
documentation.
 
Step  1  —  Choose  System  Architecture  BOM  Driver  #1  System  architecture  selection  drives  major  hardware  requirements.   ●  Addressable  vs.  Conventional  Addressable  preferred  for  most  new  
commercial/multi-family).
 ●  Voice  EVACS  vs.  Horn/Strobe.  ●  Pathway  Class  Class  A/B.   App  Output:  Selected  architecture  with  justification  notes.  
Step  2  —  Define  Required  Functions  BOM  Driver  #2  Key  functional  categories  for  the  BOM   ●  Initiation:  Pull  stations,  sprinkler  flow/supervisory,  duct/smoke,  elevator  interfaces.  ●  Notification:  Horn/strobe  or  speaker/strobe;  Public  vs.  Private  mode;  ADA  visible  
scope.
 ●  Monitoring:  Communicator  type  Cellular/IP.  ●  Annunciation:  Remote  annunciator  requirements.  
Step  3  —  Produce  the  BOM  Category-Based  Tiers)  The  BOM  is  generated  in  tiers,  accounting  for  definite  items,  rule-driven  quantities,  and  
necessary
 
allowances.
  

---

## Page 4

Tier  Description  Examples  
A  Definite  Items  Nearly  always  required  major  components.  
FACP,  power  supply,  batteries,  communicator,  surge  protection,  interface  modules.  
B  Rule-Driven  Qty  Quantities  derived  from  intake  counts.  
Monitor  modules  (per  sprinkler  riser/valve),  interface  points  (per  elevator),  pull  stations  (per  stairs/exits).  
C  Allowances  Placeholder  capacity  for  unknown  tenant  improvements  TI  or  future  needs.  
Device  allowance  per  1,000  SF,  spare  expansion  capacity.  
Step  4  —  Compliance  Check  Notes  The  "Secret  Sauce")  Each  BOM  line/category  must  be  supported  by  compliance  notes,  consistent  with  Florida  
engineering
 
rules
 
FAC
 
61G1532.
  ●  Why  included:  Trigger  condition  from  project  intake.  ●  What  it  satisfies:  NFPA  72  performance  requirement  category.  ●  What  must  be  verified  later:  E.g.,  "audibility  calcs  pending  final  reflected  ceiling  
plans."
 ●  Assumptions:  Necessary  engineering  judgments  used  in  the  calculation.  
B  Web  App  Architecture  and  Rules  
The  web  app  should  mimic  the  professional  workflow  across  four  steps,  using  a  defined  
data
 
model
 
and
 
rules
 
engine.
 
1  Core  Workflow  UI  Steps)  1.  Project  Intake  Wizard:  Guided  form  mirroring  Phase  1  data  inputs.  2.  Code  Basis  +  Requirement  Engine:  User  selects  code  cycles;  app  produces  
system
 
requirement
 
report
 
(e.g.,
 
"System
 
required:
 
yes,"
 
"Type:
 
horn/strobe,"
 
"Monitoring
 
required:
 
yes").
 3.  BOM  +  Compliance  Notes:  Generates  the  tiered  BOM  with  notes/assumptions.  4.  Kidde  Cross-Reference:  Maps  generic  specs  to  Kidde  families  and  models.  

---

## Page 5

2  Data  Model  A  relational  structure  ensures  project  data  integrity  and  clean  mapping.   ●  Project:  Contains  jurisdiction,  occupancy,  scale,  and  features.  ●  CodeBasis:  Stores  FBC,  FFPC,  NFPA  72,  NFPA  101,  and  NEC  editions.  ●  Requirement:  requirement_id,  trigger,  result  (required/optional),  citation  pointer.  ●  BOMLine:  category,  description,  quantity  (definite/rule-based/allowance),  
compliance
 
notes,
 
assumptions.
 ●  KiddeMapping:  generic  spec,  Kidde  family/model  options,  compatibility  
constraints.
 
3  Rules  Engine  Logic  The  engine  drives  the  BOM  generation  and  note  attachment.   1.  Classify  occupancy  +  features.  2.  Run  requirement  rules  to  define  required  functions.  3.  Convert  functions  to  a  generic  BOM  template.  4.  Apply  project  scale  multipliers.  5.  Attach  NFPA  72-based  compliance  notes  and  verification  checklists.   Important  Note:  Where  code  interpretation  is  provisional,  the  app  must  output:  
"Assumption:
 
"
 
and
 
"Verify
 
on
 
sheets:
 
."
 
4  Kidde  Commercial  Cross-Reference  The  cross-reference  prevents  guessing  SKUs  and  relies  on  a  structured  mapping  layer.   1.  Create  a  "Generic  Spec  BOM"  first:  E.g.,  "Addressable  FACP,  min  2  SLC,  min  2  
NAC."
 2.  Map  Generic  Spec  →  Kidde  Families:  Use  a  structured  mapping  table  (e.g.,  VS  
Series,
 
Notification
 
families).
 3.  Enforce  Compatibility:  Ensure  addressable  protocol,  power/load,  and  listed  
combinations
 
are
 
constrained.
 4.  Output:  Show  the  generic  line,  Kidde  option(s),  and  a  note:  "requires  verification  
with
 
dealer
 
submittal;
 
confirm
 
listing/compatibility."
 
C  Minimum  Viable  Product  MVP  Feature  List  
This  list  represents  the  fastest  path  to  a  professional-grade  product.   ●  Project  intake  wizard  (occupancy  +  features  +  scale).  

---

## Page 6

●  Code-basis  selector  FBC/FFPC  cycle  +  NFPA  standard  edition  basis).  ●  Requirement  report  (system  required?  voice?  monitoring?  key  interfaces?.  ●  BOM  generator  Definite  +  Rule-based  +  Allowances).  ●  Compliance  notes  per  BOM  line  (with  assumptions  +  verification  checklist).  ●  Kidde  cross-reference  (generic  →  Kidde  family  options).  ●  Export:  Excel  BOM  +  PDF  report.   

---
