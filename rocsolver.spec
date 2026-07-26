# rocSOLVER dense linear algebra (TheRock 7.14)

Name:		rocsolver
Version:	7.14.0
Release:	1
Summary:	ROCm dense linear algebra solvers (LAPACK on HIP)
License:	BSD-2-Clause
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/rocsolver.tar.gz#/rocsolver-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	rocblas-devel
BuildRequires:	rocprim-devel
BuildRequires:	pkgconfig(fmt)
BuildRequires:	lib64fmt-devel
# Sparse optional — enable when rocsparse is available
BuildRequires:	rocsparse-devel
BuildRequires:	python3

ExclusiveArch:	%{x86_64} %{aarch64}

%description
rocSOLVER provides LAPACK-like dense linear algebra solvers for HIP,
built on rocBLAS. Includes LU/QR/Cholesky factorizations, eigensolvers,
and related routines.

%package devel
Summary:	Development files for rocsolver
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel
Requires:	rocblas-devel
Provides:	rocsolver-devel = %{EVRD}

%description devel
Headers and CMake package for rocsolver.

%prep
%autosetup -n rocsolver

export CXX=hipcc
export CC=clang
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_blas} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_CLIENTS_TESTS=OFF \
	-DBUILD_CLIENTS_BENCHMARKS=OFF \
	-DBUILD_CLIENTS_SAMPLES=OFF \
	-DBUILD_TESTING=OFF \
	-DBUILD_WITH_SPARSE=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/rocsolver ] && [ ! -d %{buildroot}%{_libdir}/cmake/rocsolver ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/rocsolver %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/rocsolver/LICENSE.md
%{_libdir}/librocsolver.so.*

%files devel
%{_includedir}/rocsolver/
%{_libdir}/librocsolver.so
%{_libdir}/cmake/rocsolver/
