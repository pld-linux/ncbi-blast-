Summary:	NCBI BLAST+ finds regions of similarity between biological sequences
Name:		ncbi-blast+
Version:	2.2.29
Release:	1
License:	Public Domain and MIT
Group:		Applications/Science
Source0:	ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-%{version}+-src.tar.gz
# Source0-md5:	1290360b24448dd79840a6800482b597
Patch0:		%{name}-configure.patch
Patch1:		%{name}-libdeps.patch
URL:		http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download
BuildRequires:	boost-devel
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	fcgi-devel
BuildRequires:	freetds-devel
BuildRequires:	freetype-devel
BuildRequires:	ftgl-devel
BuildRequires:	giflib-devel
BuildRequires:	glew-devel
BuildRequires:	gnutls-devel
BuildRequires:	gsoap-devel
BuildRequires:	hdf5-c++-devel
BuildRequires:	libfuse-devel
BuildRequires:	libgcrypt
#BuildRequires:	libgssapi_krb5
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmagic-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	Mesa-libOSMesa-devel
BuildRequires:	mongodb-devel
BuildRequires:	muparser-devel
BuildRequires:	mysql-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	sablotron-devel
BuildRequires:	sqlite3-devel
BuildRequires:	wxWidgets-devel
BuildRequires:	xalan-c-devel
BuildRequires:	xerces-c-devel
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The NCBI Basic Local Alignment Search Tool (BLAST) finds regions of
local similarity between sequences. The program compares nucleotide or
protein sequences to sequence databases and calculates the statistical
significance of matches. BLAST can be used to infer functional and
evolutionary relationships between sequences as well as help identify
members of gene families.

%prep
%setup -q -n ncbi-blast-%{version}+-src
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"

cd c++
%configure \
	--with-dll \
	--with-mt \
	--without-autodep \
	--without-makefile-auto-update \
	--with-flat-makefile \
	--without-caution \
	--without-dbapi \
	--without-lzo \
	--with-runpath=%{_libdir}/ncbi-blast+ \
	--with-build-root=BUILD \
	--without-strip \
	--with-symbols

cd BUILD/build
%{__make} -f Makefile.flat all_projects="algo/blast/ app/ objmgr/ objtools/align_format/ objtools/blast/"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_libdir}/ncbi-blast+}

install -p c++/BUILD/lib/*.so $RPM_BUILD_ROOT/%{_libdir}/ncbi-blast+

cd c++/BUILD/bin
install -p blastp blastn blastx tblastn tblastx psiblast rpsblast \
	rpstblastn blast_formatter deltablast makembindex segmasker \
	dustmasker windowmasker makeblastdb makeprofiledb blastdbcmd \
	blastdb_aliastool convert2blastmask blastdbcheck legacy_blast.pl \
	blastdbcp gene_info_reader seedtop seqdb_demo seqdb_perf datatool \
	project_tree_builder update_blastdb.pl $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc c++/scripts/projects/blast/ChangeLog
%doc c++/scripts/projects/blast/README
%doc c++/scripts/projects/blast/LICENSE
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/ncbi-blast+
%attr(755,root,root) %{_libdir}/ncbi-blast+/*.so
